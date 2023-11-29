from functools import partial
from typing import Literal, Sequence

from gabenet.mcmc import sample_markov_chain
from gabenet.nets import MultinomialDirichletBelieve, PoissonGammaBelieve
from gabenet.random import PRNGSequence
from gabenet.utils import perplexity, get_hidden_unit_sizes
from gabenet._surgery import (
    copy_to_larger_net,
    prune_network,
    determine_number_to_prune,
)
import haiku as hk
import jax
from jax import random
import jax.numpy as jnp
from jaxtyping import PRNGKeyArray

from dataset import load_20newsgroups
from train_utils import TrainState, save_states


# Training hyperparameters
RANDOM_SEED = 43
N_BURNIN = 500
N_SAMPLES = 500
key_seq = PRNGSequence(jax.random.PRNGKey(RANDOM_SEED))

# Print out training hyperparameters for logging.
print(f"RANDOM_SEED = {RANDOM_SEED}")
print(f"N_BURNIN = {N_BURNIN}")
print(f"N_SAMPLES = {N_SAMPLES}")

# Model hyperparameters.
MODEL: Literal[
    "multinomial_dirichlet_believe", "poisson_gamma_believe"
] = "multinomial_dirichlet_believe"
n_topics = 200
HIDDEN_LAYER_SIZES = (n_topics,)
GAMMA_0 = 1.0
ETA = 0.05
_bottom_layer_name = (
    f"{MODEL}/~/multinomial_layer"
    if MODEL == "multinomial_dirichlet_believe"
    else f"{MODEL}/~/poisson_layer"
)
# Print out model hyperparameters for logging.
print(f"MODEL = {MODEL}")
print(f"n_topics = {n_topics}")
print(f"HIDDEN_LAYER_SIZES = {HIDDEN_LAYER_SIZES}")
print(f"GAMMA_0 = {GAMMA_0}")
print(f"ETA = {ETA}")

n_chains = jax.device_count()

X_train, X_test = load_20newsgroups()
n_features = X_train.shape[1]


if jax.device_count == 1:
    print("ERROR: Only one visible device!")
    exit(1)


@hk.transform_with_state
def kernel(n_hidden_units, X=X_train):
    """Advance the Markov chain by one step."""
    if MODEL == "multinomial_dirichlet_believe":
        model = MultinomialDirichletBelieve(
            n_hidden_units,
            n_features,
            gamma_0=GAMMA_0,
            eta=ETA,
        )
    else:
        model = PoissonGammaBelieve(
            n_hidden_units, n_features, gamma_0=GAMMA_0, eta=ETA
        )
    # Do one Gibbs sampling step.
    model(X)


def probability(params, state):
    bottom_params = params.get(_bottom_layer_name, {})
    bottom_state = state[_bottom_layer_name]
    phi = bottom_params.get("phi", bottom_state.get("phi"))
    theta = bottom_state["copy[theta(1)]"]
    probs = theta @ phi
    probs /= probs.sum(axis=-1, keepdims=True)
    return probs


def initialise(key, model_name, hidden_layer_sizes) -> TrainState:
    """Initialise training state."""
    key, subkey = random.split(key)
    keys = random.split(subkey, jax.device_count())
    params, state = jax.pmap(kernel.init)(keys)
    return TrainState(params, state, key, 0, model_name, hidden_layer_sizes)


def evaluate(params, states, X, axis=[0, 1]):
    """Compute perplexity over chains and samples by default (axis=[0, 1])."""
    probs = probability(params, states).mean(axis)
    return perplexity(X, probs)


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
    n_hidden_units: tuple[int] = (K_1max,)
    init_key_per_chain = random.split(next(key_seq), num=n_chains)
    init_fn_t = partial(kernel.init, n_hidden_units=n_hidden_units)
    params, state = jax.pmap(init_fn_t)(init_key_per_chain)
    params = jax.tree_map(lambda x: x[0], params)

    for t in range(T_max):
        print("Starting training network config:", n_hidden_units)
        # 1) Burn-in model.
        params, state_trace = sample_markov_chain(
            next(key_seq),
            kernel=partial(kernel.apply, n_hidden_units=n_hidden_units),
            n_samples=n_chains,
            n_burnin_steps=B[t],
            n_chains=n_chains,
            params=params,
            initial_state=state,
        )
        state = jax.tree_map(lambda x: x[:, -1], state_trace)  # Last state.
        loss_train = evaluate(params, state_trace, X_train)
        print(f"Training set perplexity [{MODEL}: {n_hidden_units}]: {loss_train:.2f}")
        loss_test = evaluate(params, state_trace, X_test)
        print(f"Test set perplexity: {loss_test:.2f}")
        train_state = TrainState(params, state, next(key_seq), 0, MODEL, n_hidden_units)
        save_states(train_state, state_trace)

        # Free up memory.
        del state_trace

        # 2) Prune network.
        states_pruned = []
        n_prune = determine_number_to_prune(state)
        for chain in range(n_chains):
            state_i = jax.tree_map(lambda x: x[chain], state)
            state_pruned = prune_network(state_i, n_prune)
            states_pruned.append(state_pruned)
        state_pruned = jax.tree_map(lambda *s: jnp.stack(s), *states_pruned)

        # 3) Continue training pruned network.
        n_hidden_pruned = get_hidden_unit_sizes(state_pruned)
        print("Pruned network to", n_hidden_pruned)
        params, state_trace = sample_markov_chain(
            next(key_seq),
            kernel=partial(kernel.apply, n_hidden_units=n_hidden_pruned),
            n_samples=n_samples,
            n_burnin_steps=C[t],
            n_chains=n_chains,
            params=params,
            initial_state=state_pruned,
            n_leap_size=n_leap_size,
        )
        state = jax.tree_map(lambda leaf: leaf[:, -1], state_trace)
        loss_train = evaluate(params, state_trace, X_train)
        print(f"Training set perplexity [{MODEL}: {n_hidden_units}]: {loss_train:.2f}")
        loss_test = evaluate(params, state_trace, X_test)
        print(f"Test set perplexity: {loss_test:.2f}")
        train_state = TrainState(params, state, next(key_seq), 0, MODEL, n_hidden_units)
        save_states(train_state, state_trace)

        del state_trace

        # Add new layer with same size as top layer after pruning.
        n_hidden_units = n_hidden_pruned[:1] + n_hidden_pruned

        # 4) Copy parameters and state to new network config.
        init_key_per_chain = random.split(next(key_seq), num=n_chains)
        init_fn_t = partial(kernel.init, n_hidden_units=n_hidden_units)
        params_target, state_target = jax.pmap(init_fn_t)(init_key_per_chain)
        params, state = copy_to_larger_net(params, state, params_target, state_target)


greedy_layer_wise_training(
    next(key_seq),
    kernel,
    n_samples=N_SAMPLES,
    T_max=3,
    K_1max=n_topics,
    B=[N_BURNIN * 2, N_BURNIN, N_BURNIN],
    C=[0, 0, 0],
    n_leap_size=5,
)
