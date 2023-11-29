from functools import partial
from typing import Any, Callable, Optional, Sequence
import warnings

import haiku as hk
import jax
from jax import random
import jax.numpy as jnp
from jax.tree_util import tree_map
from jaxtyping import Array, PRNGKeyArray, PyTree, UInt

from mubelnet.sugar import scannable
from mubelnet._surgery import (
    copy_to_larger_net,
    determine_number_to_prune,
    prune_network,
)
from mubelnet.utils import get_hidden_unit_sizes


def sample_markov_chain(
    key,
    kernel: Callable[[tuple], tuple[Any, dict]] | hk.TransformedWithState,
    n_samples: int,
    n_burnin_steps: int,
    n_chains: Optional[int] = None,
    params: Optional[hk.Params] = None,
    initial_state: Optional[hk.State] = None,
    n_leap_size: int = 1,
):
    """Take samples using Markov chain Monte Carlo.

    Args:
        key: Pseudo random number generator key.
        kernel: The transition kernel that advances the Markov chain by one step. The
            kernel is either a haiku `TransformedWithState` or a function compatible
            with `TransformedWithState.apply`.
        n_samples: Number of samples to generate.
        n_burnin_steps: Advance the chain by this many steps before taking a sample.
        n_chains: Number of (independent) Markov chains to run.
        params: The state-independent `params` (a pytree) of
            the Markov chain. When `None`, kernel is assumed to be a
            `TransformedWithState` to initialise using `kernel.init`.
        initial_state: Starting `state` (a pytree) of the Markov chain. Leading
            dimension corresponds to a chain.
        n_leap_size: Number of successive steps between samples.

    Returns:
        A pair of `(params, state)`, each a pytree. The leading dimension of
        `params` and `state` refers to the chain. The second dimension of `state`
        corresponds to the samples in per chain.
    """
    key_seq = hk.PRNGSequence(key)

    _scannable_kernel_fn = scannable(kernel)

    if initial_state is None or params is None:
        if not isinstance(kernel, hk.TransformedWithState):
            raise ValueError(
                "Kernel must be `TransformedWithState` to be able to initialise"
                "`params` and `state` when either is None."
            )
        if n_chains is None:
            raise ValueError("Number of chains not specified!")

        init_key_per_chain = random.split(next(key_seq), num=n_chains)
        params, initial_state = jax.vmap(kernel.init)(init_key_per_chain)
        params = jax.tree_map(lambda x: x[0], params)
    else:
        states_leaves = jax.tree_util.tree_leaves(initial_state)
        # Leading axis of states corresponds to chains.
        n_chains_expected = states_leaves[0].shape[0]
        if n_chains is None:
            n_chains = n_chains_expected
        elif n_chains != n_chains_expected:
            raise ValueError(
                f"The leading axis of `initial_state` suggests "
                f"{n_chains_expected} chains, but the argument is set to "
                f"`n_chains={n_chains}`."
            )

    n_samples_per_chain = n_samples // n_chains

    def _leapfrog(carry, _):
        """A for-loop (from 0,..,`n_steps-1`) that runs `step`."""
        carry_out, _ = jax.lax.scan(
            _scannable_kernel_fn, carry, xs=None, length=n_leap_size
        )
        state = carry_out[1]
        return carry_out, state

    def _sampler(params_init, state_init, key):
        """Samper for a single Markov chain."""
        carry = (params_init, state_init, key)
        # 1) Take first sample after `(n_burnin - n_leap_size) + n_leap_size` steps.
        carry, _ = jax.lax.scan(
            _scannable_kernel_fn, carry, xs=None, length=n_burnin_steps - n_leap_size
        )
        # 2) Take subsequent samples after `n_leap_size` steps.
        carry, stacked_states = jax.lax.scan(
            _leapfrog, carry, xs=None, length=n_samples_per_chain
        )

        return stacked_states

    n_devices = jax.local_device_count()

    if n_devices == 1:
        warnings.warn("Only one visible device in JAX. Reconfigure XLA_FLAGS.")

    if n_devices == n_chains:
        # Run each chain on a separate device.
        _vectorised_kernel_fn = jax.pmap(_sampler, in_axes=(None, 0, 0))
    else:
        # Vectorise with vmap instead of sharding across devices.
        warnings.warn(
            f"Chains (n={n_chains}) not divisible across devices. Falling back to vmap."
        )
        _vectorised_kernel_fn = jax.vmap(_sampler, in_axes=(None, 0, 0))

    if n_samples % n_chains > 0:
        raise ValueError(
            "Number of samples {n_samples} not divisible by {n_chains} chains."
        )

    # Generate an initial state for each chain.
    keys = random.split(next(key_seq), num=n_chains)

    state = _vectorised_kernel_fn(params, initial_state, keys)
    return params, state


def greedy_layer_wise_training(
    key: PRNGKeyArray,
    kernel: hk.TransformedWithState,
    n_samples: int,
    T_max: int,
    K_1max: int,
    B: Sequence[int],
    C: Sequence[int],
    n_leap_size: int = 1,
):
    """Layer-wise training strategy to greedily infer the network configuration.

    See Algorithm 1. (p. 34) of the Zhou-Cong-Chen paper.
    References:
        Zhou-Cong-Chen. J. Mach. Learn. Res. 17.1, p. 34 (2016).

    Args:
        key: Pseudo random number generator key.
        kernel: The transition kernel that advances the Markov chain by one step. The
            kernel is a haiku `TransformedWithState` based on a function that takes as
            argument the keyword `n_hidden_units`: a tuple indicating the network size.
        n_samples: Number of posterior samples to collect for each layer.
        K_1max: Maximum width of the first layer.
        T_max: Maximum number of layers to train.
        B: Per layer, the number of Gibbs iterations _before_ pruning.
        C: Per layer, the number of Gibbs burn-in iterations _after_ pruning.
        n_leap_size: Number of successive steps between collected samples.

    Returns:
        A pair of dicts: params and states. The dicts contain for each network
        configuration (key), the params and a trace of the states, respectively.

    """
    key_seq = hk.PRNGSequence(key)
    n_chains = jax.device_count()

    # 0)
    n_hidden_units: tuple[int, ...] = (K_1max,)
    init_key_per_chain = random.split(next(key_seq), num=n_chains)
    init_fn_t = partial(kernel.init, n_hidden_units=n_hidden_units)
    params, state = jax.pmap(init_fn_t)(init_key_per_chain)
    params = jax.tree_map(lambda x: x[0], params)

    # Collect posterior samples, per network config, in this variable.
    state_traces_result: dict[tuple, PyTree] = {}
    params_result: dict[tuple, PyTree] = {}

    for t in range(T_max):
        print("Starting training network config:", n_hidden_units)

        kernel_fn = jax.pmap(
            partial(kernel.apply, n_hidden_units=n_hidden_units), in_axes=(None, 0, 0)
        )
        # 1) Burn-in model.
        for _ in range(B[t]):
            _, state = kernel_fn(params, state, random.split(next(key_seq), n_chains))

        # 2) Prune network.
        states_pruned = []
        n_prune = determine_number_to_prune(state)
        for chain in range(n_chains):
            state_i = jax.tree_map(lambda x: x[chain], state)
            state_pruned = prune_network(state_i, n_prune)
            states_pruned.append(state_pruned)
        state = jax.tree_map(lambda *s: jnp.stack(s), *states_pruned)

        # 3) Continue training pruned network.
        n_hidden_pruned = get_hidden_unit_sizes(state)
        print("Pruned network to", n_hidden_pruned)
        kernel_fn = jax.pmap(
            partial(kernel.apply, n_hidden_units=n_hidden_pruned), in_axes=(None, 0, 0)
        )
        for _ in range(C[t]):
            _, state = kernel_fn(params, state, random.split(next(key_seq), n_chains))

        state_trace = []
        for i in range(n_samples * n_leap_size):
            _, state = kernel_fn(params, state, random.split(next(key_seq), n_chains))
            if i % n_leap_size == 0:
                state_trace.append(state)
        state_trace = tree_map(lambda *x: jnp.stack(x, axis=1), *state_trace)

        state_traces_result[n_hidden_pruned] = state_trace
        params_result[n_hidden_pruned] = params

        del state_trace

        # Add new layer with same size as top layer after pruning.
        n_hidden_units = n_hidden_pruned[:1] + n_hidden_pruned

        # 4) Copy parameters and state to new network config.
        init_key_per_chain = random.split(next(key_seq), num=n_chains)
        init_fn_t = partial(kernel.init, n_hidden_units=n_hidden_units)
        params_target, state_target = jax.pmap(init_fn_t)(init_key_per_chain)
        params, state = copy_to_larger_net(params, state, params_target, state_target)

    return params_result, state_traces_result
