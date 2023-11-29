from unittest import TestCase

# Run the following before any XLA modules such as JAX:
import chex

chex.set_n_cpu_devices(6)

import jax
from jax import random
import haiku as hk

from mubelnet.mcmc import sample_markov_chain
from mubelnet.nets import MultinomialBelief


key_seq = hk.PRNGSequence(42)
m_samples = 11
n_features = 7

X_train = random.randint(
    next(key_seq),
    shape=(m_samples, n_features),
    minval=0,
    maxval=10,
)


@hk.transform_with_state
def kernel():
    model = MultinomialBelief(input_sizes=[4, 2], output_size=n_features)
    model(X_train)


class TestSampler(TestCase):
    def test_haiku_kernel(self):
        """Test kernel as a haiku transform."""
        n_chains = 3
        n_samples_per_chain = 2

        # 1) Sample using kernel.
        params, state = sample_markov_chain(
            next(key_seq),
            kernel,
            n_samples=n_chains * n_samples_per_chain,
            n_burnin_steps=2,
            n_chains=n_chains,
        )

        chex.assert_tree_shape_prefix(state, (n_chains, n_samples_per_chain))

        # 2) Continue sampling the chain.
        last_state = jax.tree_util.tree_map(lambda x: x[:, -1, ...], state)
        _, new_state = sample_markov_chain(
            next(key_seq),
            kernel,
            n_samples=n_chains,
            n_burnin_steps=0,
            initial_state=last_state,
            params=params,
        )
        chex.assert_tree_shape_prefix(new_state, (n_chains, 1))

        # We require a `hk.TransformedWithState` when no state_init and params are
        # provided.
        with self.assertRaises(ValueError):
            params, state = sample_markov_chain(
                next(key_seq),
                kernel.apply,
                n_samples=n_chains * n_samples_per_chain,
                n_burnin_steps=2,
                n_chains=n_chains,
            )

    def test_kernel_function(self):
        """Test kernel as a function."""
        n_chains = 1
        n_samples_per_chain = 1

        keys = random.split(next(key_seq), num=n_chains)
        params, state_init = jax.vmap(kernel.init)(keys)

        _, state = sample_markov_chain(
            next(key_seq),
            kernel.apply,
            n_burnin_steps=0,
            n_samples=n_samples_per_chain * n_chains,
            initial_state=state_init,
            params=params,
        )
        chex.assert_tree_shape_prefix(state, (n_chains, n_samples_per_chain))
