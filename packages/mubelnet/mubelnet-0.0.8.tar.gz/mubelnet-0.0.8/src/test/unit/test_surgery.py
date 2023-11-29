from unittest import TestCase

import haiku as hk
from jax import random
import jax.numpy as jnp
from numpy.testing import assert_array_equal, assert_allclose

from mubelnet.nets import PoissonGammaBelief, MultinomialBelief
from mubelnet._surgery import copy_to_larger_net, prune_network


m_samples = 11
n_features = 7

X_train = random.randint(
    random.PRNGKey(43),
    shape=(m_samples, n_features),
    minval=0,
    maxval=10,
)


@hk.transform_with_state
def kernel_pgbn(n_hidden_units):
    model = PoissonGammaBelief(input_sizes=n_hidden_units, output_size=n_features)
    model.layers.layers[-1].set_training(False)  # Freeze phi in the bottom layer.
    model(X_train)


@hk.transform_with_state
def kernel_mdbn(n_hidden_units):
    model = MultinomialBelief(input_sizes=n_hidden_units, output_size=n_features)
    model.layers.layers[-1].set_training(False)  # Freeze phi in the bottom layer.
    model(X_train)


class TestModelSurgery(TestCase):
    def setUp(self):
        self.key_seq = hk.PRNGSequence(42)

    def test_shapes_after_network_pruning(self):
        """Test that network is consistently pruned."""
        params_source, state_source = kernel_pgbn.init(
            next(self.key_seq), n_hidden_units=(4, 8)
        )
        _, state_source = kernel_pgbn.apply(
            params_source, state_source, next(self.key_seq), n_hidden_units=(4, 8)
        )
        state_pruned = prune_network(state_source, 2)
        is_zero = state_source["poisson_gamma_belief/~/cap_layer"]["m_k"] == 0
        n_pruned = int(is_zero.sum())
        # Test that both theta in the top and phi in the layer below are pruned.
        n_expected = 4 - n_pruned
        n_actual = state_pruned["poisson_gamma_belief/~/cap_layer"]["theta"].shape[1]
        self.assertEqual(n_actual, n_expected)

        n_actual = state_pruned["poisson_gamma_belief/~/gamma_layer"]["phi"].shape[0]
        self.assertEqual(n_actual, n_expected)

        # Check that the cache is also pruned.
        n_actual = state_pruned["poisson_gamma_belief/~/gamma_layer"][
            "copy[theta(t+1)]"
        ].shape[1]
        self.assertEqual(n_actual, n_expected)

    def test_normalisation_after_pruning(self):
        """Test that after pruning all variables are properly normalised."""
        # 1)
        # Verify that for the multinomial belief the parameters are re-normalised.
        params_mdbn_source, state_mdbn_source = kernel_mdbn.init(
            next(self.key_seq), n_hidden_units=(4, 8)
        )
        _, state_mdbn_source = kernel_mdbn.apply(
            params_mdbn_source,
            state_mdbn_source,
            next(self.key_seq),
            n_hidden_units=(4, 8),
        )
        state_mdbn_pruned = prune_network(state_mdbn_source, 2)
        theta_2 = state_mdbn_pruned["multinomial_belief/~/cap_layer"]["theta"]
        theta_2_norm = theta_2.sum(axis=1)
        assert_allclose(theta_2_norm, 1.0, rtol=1e-6)

        # Test normalisation of `r` in caplayer.
        r = state_mdbn_pruned["multinomial_belief/~/cap_layer"]["r"]
        r_norm = r.sum()
        assert_allclose(r_norm, 1.0, rtol=1e-6)

        theta_1 = state_mdbn_pruned["multinomial_belief/~/dirichlet_layer"]["theta"]
        theta_1_norm = theta_1.sum(axis=1)
        assert_allclose(theta_1_norm, 1.0, rtol=1e-6)

        phi_1 = state_mdbn_pruned["multinomial_belief/~/dirichlet_layer"]["phi"]
        phi_1_norm = phi_1.sum(axis=-1)
        assert_allclose(phi_1_norm, 1.0, rtol=1e-6)

        # 2)
        # But also check that this is not done for the Poisson gamma belief net.
        params_pgbn_source, state_pgbn_source = kernel_pgbn.init(
            next(self.key_seq), n_hidden_units=(4, 8)
        )
        _, state_pgbn_source = kernel_pgbn.apply(
            params_pgbn_source,
            state_pgbn_source,
            next(self.key_seq),
            n_hidden_units=(4, 8),
        )
        state_pgbn_pruned = prune_network(state_pgbn_source, 2)
        theta_2 = state_pgbn_pruned["poisson_gamma_belief/~/cap_layer"]["theta"]
        theta_2_norm = theta_2.sum(axis=1)
        self.assertFalse(jnp.allclose(theta_2_norm, 1.0, rtol=1e-6))

        # Test normalisation of `r` in caplayer.
        r = state_pgbn_pruned["poisson_gamma_belief/~/cap_layer"]["r"]
        r_norm = r.sum()
        self.assertFalse(jnp.allclose(r_norm, 1.0, rtol=1e-6))

        theta_1 = state_pgbn_pruned["poisson_gamma_belief/~/gamma_layer"]["theta"]
        theta_1_norm = theta_1.sum(axis=1)
        self.assertFalse(jnp.allclose(theta_1_norm, 1.0, rtol=1e-6))

        # However, the phi should still be normalised.
        phi_1 = state_pgbn_pruned["poisson_gamma_belief/~/gamma_layer"]["phi"]
        phi_1_norm = phi_1.sum(axis=-1)
        assert_allclose(phi_1_norm, 1.0, rtol=1e-6)

    def test_copy_to_new_net(self):
        """Test that all parameters are correctly copied."""
        # Original network.
        params_source, state_source = kernel_pgbn.init(
            next(self.key_seq), n_hidden_units=(4, 8)
        )
        # New network with extra layer.
        params_target, state_target = kernel_pgbn.init(
            next(self.key_seq), n_hidden_units=(4, 4, 8)
        )

        new_params, new_state = copy_to_larger_net(
            params_source, state_source, params_target, state_target
        )
        # Check that theta is correctly moved to new network.
        expected = state_source["poisson_gamma_belief/~/cap_layer"]["theta"]
        actual = new_state["poisson_gamma_belief/~/gamma_layer"]["theta"]
        assert_array_equal(expected, actual)

        # Verify that also the theta copy was moved.
        copy_name = "copy[theta(t+1)]"
        expected = state_source["poisson_gamma_belief/~/gamma_layer"][copy_name]
        actual = new_state["poisson_gamma_belief/~/gamma_layer_1"][copy_name]
        assert_array_equal(expected, actual)

        # Check that theta is correctly moved to new network.
        expected = state_source["poisson_gamma_belief/~/gamma_layer"]["theta"]
        actual = new_state["poisson_gamma_belief/~/gamma_layer_1"]["theta"]
        assert_array_equal(expected, actual)

        # Verify that also the theta copy was moved.
        copy_name = "copy[theta(1)]"
        expected = state_source["poisson_gamma_belief/~/poisson_layer"][copy_name]
        actual = new_state["poisson_gamma_belief/~/poisson_layer"][copy_name]
        assert_array_equal(expected, actual)

        # Check that theta is correctly moved to new network.
        expected = state_source["poisson_gamma_belief/~/gamma_layer"]["phi"]
        actual = new_state["poisson_gamma_belief/~/gamma_layer_1"]["phi"]
        assert_array_equal(expected, actual)

        # Check that theta is correctly moved to new network.
        expected = state_source["poisson_gamma_belief/~/gamma_layer"]["c"]
        actual = new_state["poisson_gamma_belief/~/gamma_layer_1"]["c"]
        assert_array_equal(expected, actual)

        # Check that theta is correctly moved to new network.
        expected = state_source["poisson_gamma_belief/~/cap_layer"]["c"]
        actual = new_state["poisson_gamma_belief/~/gamma_layer"]["c"]
        assert_array_equal(expected, actual)

        expected = params_source["poisson_gamma_belief/~/poisson_layer"]["phi"]
        actual = new_params["poisson_gamma_belief/~/poisson_layer"]["phi"]
        assert_array_equal(expected, actual)
