from functools import partial
from unittest import skip

# Run the following before any XLA modules such as JAX:
import chex

chex.set_n_cpu_devices(6)

from scipy.stats import entropy
import haiku as hk
import jax
import jax.numpy as jnp
from jax import random
import numpy as np

from mubelnet.calibration import simulation_based_calibration
from mubelnet.nets import MultinomialBelief, PoissonGammaBelief
from mubelnet.sugar import scannable

from test import TestCase


# Network configuration.
m_samples = 11
n_features = 7
n_components2 = 2
n_components1 = 4
network_size = (n_components2, n_components1)


def build_poisson_network(is_training):
    # Choose gamma_0 that gives dense (instead of sparse) data. Technically, the gamma
    # distribution can never be zero. Due to finite precision, all small non-zero values
    # collapse to zero. This makes simulation based calibration, which relies on the
    # ranking of the values problematic.
    # Choosing gamma_0 > n_components2 leads to a shape (of the norm of `r`) that
    # is > 1. A shape > 1 is dense.
    gamma_0 = n_components2 + 0.5

    return PoissonGammaBelief(
        network_size,
        n_features,
        is_training=is_training,
        # Reduce variance of `c` by half, to prevent:
        # small `c` => large `theta's` => large X => large computation time.
        e_0=2.0,
        f_0=2.0,
        #
        gamma_0=gamma_0,
    )


@hk.transform_with_state
@chex.assert_max_traces(1)
def forward_poisson_gamma_net(is_training: bool = True, num_samples=m_samples):
    model = build_poisson_network(is_training)
    return model.forward(num_samples)


def build_multinomial_network(is_training):
    gamma_0 = n_components2 + 0.5
    model = MultinomialBelief(
        network_size,
        n_features,
        gamma_0=gamma_0,
        e_0=gamma_0,
        is_training=is_training,
    )
    return model


@hk.transform_with_state
@chex.assert_max_traces(1)
def forward_mult_dir_net(is_training: bool = True, num_samples=m_samples):
    model = build_multinomial_network(is_training)
    return model.forward(num_samples)


@hk.transform_with_state
@chex.assert_max_traces(2)
def step_poisson_gamma_net(x_ip, is_training: bool = True):
    model = build_poisson_network(is_training)
    model(x_ip)


@hk.transform_with_state
@chex.assert_max_traces(2)
def step_mult_dir_net(x_ip, is_training: bool = True):
    model = build_multinomial_network(is_training)
    model(x_ip)


@partial(jax.pmap, in_axes=(0, None, None), static_broadcasted_argnums=2)
def _poisson_gamma_net_sampler(key, X_train, n_samples: int):
    """After `n_burnin` steps, take `n_samples` after `n_leap_size` steps each."""
    n_burnin: int = 2_000
    n_leap_size: int = 1_000
    step = scannable(step_poisson_gamma_net)

    def _leapfrog(carry, _):
        """A for-loop (from 0,..,`n_steps-1`) that runs `step`."""
        carry_out, _ = jax.lax.scan(step, carry, xs=None, length=n_leap_size)
        state = carry_out[1]
        return carry_out, state

    # Initialise Markov chains using a forward sample state.
    key, sub_key = random.split(key)
    _, state_init = forward_poisson_gamma_net.init(sub_key, num_samples=len(X_train))

    # Collect a sample (n_samples in total) after the following number of Gibbs steps:
    # n_burnin, n_leap_size, ..., n_leapsize.
    carry = (None, state_init, key, X_train)
    carry, _ = jax.lax.scan(step, carry, None, length=n_burnin - n_leap_size)
    carry, stacked_states = jax.lax.scan(_leapfrog, carry, xs=None, length=n_samples)

    return stacked_states


@partial(jax.pmap, in_axes=(0, None, None), static_broadcasted_argnums=2)
def _mult_dir_net_sampler(key, X_train, n_samples: int):
    """After `n_burnin` steps, take `n_samples` after `n_leap_size` steps each."""
    n_burnin: int = 2_000
    n_leap_size: int = 1_000

    step = scannable(step_mult_dir_net)

    def _leapfrog(carry, _):
        """A for-loop (from 0,..,`n_steps-1`) that runs `step`."""
        carry_out, _ = jax.lax.scan(step, carry, xs=None, length=n_leap_size)
        state = carry_out[1]
        return carry_out, state

    # Initialise Markov chains using a forward sample state.
    key, sub_key = random.split(key)
    _, state_init = forward_mult_dir_net.init(sub_key, num_samples=len(X_train))

    # Collect a sample (n_samples in total) after the following number of Gibbs steps:
    # n_burnin, n_leap_size, ..., n_leapsize.
    carry = (None, state_init, key, X_train)
    carry, _ = jax.lax.scan(step, carry, xs=None, length=n_burnin - n_leap_size)
    carry, stacked_states = jax.lax.scan(_leapfrog, carry, xs=None, length=n_samples)

    return stacked_states


def mult_dir_net_sampler(key, X_train, n_samples):
    n_chains = jax.local_device_count()
    n_samples_per_chain = n_samples // n_chains
    keys = random.split(key, num=n_chains)
    states = _mult_dir_net_sampler(keys, X_train, n_samples_per_chain)
    return states


def poisson_gamma_net_sampler(key, X_train, n_samples):
    n_chains = jax.local_device_count()
    n_samples_per_chain = n_samples // n_chains
    keys = random.split(key, num=n_chains)
    states = _poisson_gamma_net_sampler(keys, X_train, n_samples_per_chain)
    return states


class TestCompletePoissonGammaBelief(TestCase):
    """Test the Gamma layer in conjuction with the Poisson layer."""

    def setUp(self):
        self.key_seq = hk.PRNGSequence(42)

    def test_training_mode(self):
        """Test setting training and inference mode."""
        # Arbitrary input data to test on.
        x_observed = random.randint(
            next(self.key_seq), shape=(m_samples, n_features), minval=0, maxval=10
        )

        # Test that trainable parameters are in state but not in params.
        params, state = forward_poisson_gamma_net.init(
            next(self.key_seq), is_training=True
        )

        _, state = step_poisson_gamma_net.apply(
            params, state, next(self.key_seq), x_observed, is_training=True
        )
        self.assertIn("r", state["poisson_gamma_belief/~/cap_layer"])
        self.assertIn("phi", state["poisson_gamma_belief/~/poisson_layer"])
        self.assertIn("phi", state["poisson_gamma_belief/~/gamma_layer"])

        self.assertNotIn("phi", params.get("poisson_gamma_belief/~/poisson_layer", {}))
        self.assertNotIn("r", params.get("poisson_gamma_belief/~/cap_layer", {}))
        self.assertNotIn("phi", params.get("poisson_gamma_belief/~/gamma_layer", {}))

        # Test that frozen parameters are in params but not in state.
        params, state = forward_poisson_gamma_net.init(
            next(self.key_seq), is_training=False
        )
        _, state = step_poisson_gamma_net.apply(
            params, state, next(self.key_seq), x_observed, is_training=False
        )
        self.assertIn("phi", params["poisson_gamma_belief/~/poisson_layer"])
        self.assertIn("r", params["poisson_gamma_belief/~/cap_layer"])
        self.assertIn("phi", params["poisson_gamma_belief/~/gamma_layer"])

        self.assertNotIn("phi", state.get("poisson_gamma_belief/~/poisson_layer", {}))
        self.assertNotIn("r", state.get("poisson_gamma_belief/~/cap_layer", {}))
        self.assertNotIn("phi", state.get("poisson_gamma_belief/~/gamma_layer", {}))

    def test_poisson_gamma_belief_net_log_likelihood(self):
        """Test symmetries of log-likelihood."""

        @hk.without_apply_rng
        @hk.transform_with_state
        def joint_log_likelihood(x_observed):
            model = build_poisson_network(is_training=False)
            if hk.running_init():
                # Initialise states with ancestral samples.
                model.init(x_observed)
            return model.joint_log_prob(x_observed)

        # Arbitrary input data to test on.
        x_observed = random.randint(
            next(self.key_seq), shape=(m_samples, n_features), minval=0, maxval=10
        )
        params, state = joint_log_likelihood.init(next(self.key_seq), x_observed)
        log_prob, state = joint_log_likelihood.apply(params, state, x_observed)

        # Test latent state permutation invariance of log-likelihood.
        state_permuted = state.copy()
        params_permuted = params.copy()

        # Permute latent states of the top layer.
        params_permuted["poisson_gamma_belief/~/cap_layer"]["r"] = jnp.roll(
            params["poisson_gamma_belief/~/cap_layer"]["r"], 1, axis=0
        )
        state_permuted["poisson_gamma_belief/~/cap_layer"]["theta"] = jnp.roll(
            state["poisson_gamma_belief/~/cap_layer"]["theta"], 1, axis=1
        )
        # Permute latent states of the bottom layer.
        state_permuted["poisson_gamma_belief/~/gamma_layer"]["theta"] = jnp.roll(
            state["poisson_gamma_belief/~/gamma_layer"]["theta"], 1, axis=1
        )
        # Permute phi two times, since layer 1 and layer 2 are both permuted.
        params_permuted["poisson_gamma_belief/~/gamma_layer"]["phi"] = jnp.roll(
            jnp.roll(params["poisson_gamma_belief/~/gamma_layer"]["phi"], 1, axis=0),
            1,
            axis=1,
        )
        params_permuted["poisson_gamma_belief/~/poisson_layer"]["phi"] = jnp.roll(
            params["poisson_gamma_belief/~/poisson_layer"]["phi"], 1, axis=0
        )
        log_prob_permuted, _ = joint_log_likelihood.apply(
            params, state_permuted, x_observed
        )

        self.assertTrue(jnp.allclose(log_prob, log_prob_permuted))

    def test_calibration_without_observations(self):
        """Test that the posterior sampler recovers prior in absence of observations."""

        def summarise_state_fn(state):
            bottom_layer = state["poisson_gamma_belief/~/poisson_layer"]
            middle_layer = state["poisson_gamma_belief/~/gamma_layer"]
            cap_layer = state["poisson_gamma_belief/~/cap_layer"]

            r_norm = cap_layer["r"].sum(axis=-1, keepdims=True)
            entropy_r = entropy(cap_layer["r"] / r_norm, axis=-1)

            phi_1_squared = jnp.sum(bottom_layer["phi"] ** 2, axis=-2)
            entropy_phi_2 = jnp.sum(entropy(middle_layer["phi"], axis=-1), axis=-1)

            summary = {
                "cap_layer": {"|r|": r_norm.squeeze(), "entropy(r)": entropy_r},
                "middle_layer": {"sum_k entropy[phi_2(k)]": entropy_phi_2},
                "bottom_layer": {"|phi^2|": phi_1_squared},
            }
            return summary

        empty_forward = hk.TransformedWithState(
            init=partial(forward_poisson_gamma_net.init, num_samples=m_samples),
            apply=partial(forward_poisson_gamma_net.apply, num_samples=m_samples),
        )

        histogram = simulation_based_calibration(
            forward_fn=empty_forward,
            posterior_fn=poisson_gamma_net_sampler,
            key=next(self.key_seq),
            state_fn=summarise_state_fn,
            n_replicates=480,
            n_posterior_samples=12,
        )

        n_tests = n_features
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        # Test ranking uniformity of phi_kj for each channel k and feature j.
        histogram_phi_1 = histogram["bottom_layer"]["|phi^2|"]
        for j in range(n_features):
            with self.subTest(feature=j, variable="|phi^2(j)|", layer="bottom"):
                self.assertUniform(
                    histogram_phi_1[..., j], alpha=alpha, name=f"norm_phi_j{j}"
                )

        # Test ranking uniformity of phi_kj for each channel k and feature j.
        hist_S_phi2 = histogram["middle_layer"]["sum_k entropy[phi_2(k)]"]
        alpha = min(self.false_positive_rate, 0.01)
        with self.subTest(variable="sum_k entropy[phi_2(k)]", layer="middle"):
            self.assertUniform(hist_S_phi2, alpha=alpha, name="entropy_mid_phi")

        alpha = min(self.false_positive_rate, 0.01)
        with self.subTest(variable="|r|", layer="cap"):
            self.assertUniform(
                histogram["cap_layer"]["|r|"], alpha=alpha, name="r_norm"
            )

        alpha = min(self.false_positive_rate, 0.01)
        hist_r_entr = histogram["cap_layer"]["entropy(r)"]
        with self.subTest(variable="entropy(r)"):
            self.assertUniform(hist_r_entr, alpha=alpha, name="entropy_r")

    @skip("Skip this long failing calibration test.")
    def test_poisson_gamma_belief_net(self):
        """Test posterior sampler of Poisson gamma belief network."""
        n_chains = jax.local_device_count()
        self.assertGreater(n_chains, 1)

        def summarise_state_fn(state):
            bottom_layer = state["poisson_gamma_belief/~/poisson_layer"]
            middle_layer = state["poisson_gamma_belief/~/gamma_layer"]
            cap_layer = state["poisson_gamma_belief/~/cap_layer"]
            a_1 = middle_layer["theta"] @ bottom_layer["phi"]
            a_2 = cap_layer["theta"] @ middle_layer["phi"]

            # Add little error to prevent zero division.
            a_1 = a_1 + 1.1754944e-38
            a_2 = a_2 + 1.1754944e-38

            r_norm = cap_layer["r"].sum(axis=-1, keepdims=True)
            entropy_r = entropy(cap_layer["r"] / r_norm, axis=-1)
            a_1_norm = a_1.sum(axis=-1, keepdims=True)
            a_2_norm = a_2.sum(axis=-1, keepdims=True)
            entropy_1 = entropy(a_1 / a_1_norm, axis=-1)
            entropy_2 = entropy(a_2 / a_2_norm, axis=-1)

            phi_1_squared = jnp.sum(bottom_layer["phi"] ** 2, axis=-2)
            entropy_phi_2 = jnp.sum(entropy(middle_layer["phi"], axis=-1), axis=-1)

            summary = {
                "cap_layer": {
                    "c": cap_layer["c"],
                    "|r|": r_norm.squeeze(),
                    "entropy(r)": entropy_r,
                },
                "middle_layer": {
                    "c": middle_layer["c"],
                    "sum_k entropy[phi_2(k)]": entropy_phi_2,
                    "a_2_norm": a_2_norm.squeeze(),
                    "entropy": entropy_2,
                },
                "bottom_layer": {
                    "activation": a_1,
                    "entropy": entropy_1,
                    "|phi^2|": phi_1_squared,
                },
            }
            return summary

        histogram = simulation_based_calibration(
            forward_fn=forward_poisson_gamma_net,
            posterior_fn=poisson_gamma_net_sampler,
            key=next(self.key_seq),
            state_fn=summarise_state_fn,
            n_replicates=480,
            n_posterior_samples=12,
        )

        n_tests = n_features
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        # Test ranking uniformity of phi_kj for each channel k and feature j.
        histogram_phi_1 = histogram["bottom_layer"]["|phi^2|"]
        for j in range(n_features):
            with self.subTest(feature=j, variable="|phi^2(j)|", layer="bottom"):
                self.assertUniform(
                    histogram_phi_1[..., j], alpha=alpha, name=f"norm_phi_j{j}"
                )

        # Test ranking uniformity of phi_kj for each channel k and feature j.
        hist_S_phi2 = histogram["middle_layer"]["sum_k entropy[phi_2(k)]"]
        alpha = min(self.false_positive_rate, 0.01)
        with self.subTest(variable="sum_k entropy[phi_2(k)]", layer="middle"):
            self.assertUniform(hist_S_phi2, alpha=alpha, name="entropy_mid_phi")

        n_tests = m_samples * n_features
        hist_activation1 = histogram["bottom_layer"]["activation"]
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        for i in range(m_samples):
            for j in range(n_features):
                with self.subTest(
                    variable="activation(i,j)", sample=i, feature=j, layer="bottom"
                ):
                    self.assertUniform(
                        hist_activation1[..., i, j],
                        alpha=alpha,
                        name=f"activation__{i}_{j}",
                    )

        n_tests = m_samples
        hist_a2_norm = histogram["middle_layer"]["a_2_norm"]
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        for i in range(m_samples):
            with self.subTest(variable="|activation(i)|", layer="middle", sample=i):
                self.assertUniform(
                    hist_a2_norm[..., i], alpha=alpha, name=f"mid_activation_{i}"
                )

        n_tests = m_samples
        hist_entropy2 = histogram["middle_layer"]["entropy"]
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        for i in range(m_samples):
            with self.subTest(
                variable="entropy[activation(i)]", sample=i, layer="middle"
            ):
                self.assertUniform(
                    hist_entropy2[..., i], alpha=alpha, name=f"entropy_activ_{i}"
                )

        alpha = min(self.false_positive_rate, 0.01)
        with self.subTest(variable="|r|", layer="cap"):
            self.assertUniform(
                histogram["cap_layer"]["|r|"], alpha=alpha, name="r_norm"
            )

        alpha = min(self.false_positive_rate, 0.01)
        hist_r_entr = histogram["cap_layer"]["entropy(r)"]
        with self.subTest(variable="entropy(r)"):
            self.assertUniform(hist_r_entr, alpha=alpha, name="entropy_r")

        hist_c2 = histogram["cap_layer"]["c"]
        n_tests = m_samples
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        for i in range(m_samples):
            with self.subTest(sample=i, layer="cap", variable="c"):
                self.assertUniform(hist_c2[..., i], alpha=alpha, name=f"cap_c_{i}")

        hist_c1 = histogram["middle_layer"]["c"]
        n_tests = m_samples
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        for i in range(m_samples):
            with self.subTest(sample=i, layer="middle", variable="c"):
                self.assertUniform(hist_c1[..., i], alpha=alpha, name=f"mid_c_{i}")


class TestCompleteMultinomialDirichletBelief(TestCase):
    """Test the Gamma layer in conjuction with the Poisson layer."""

    def setUp(self):
        self.key_seq = hk.PRNGSequence(42)

    def test_multinomial_belief_log_likelihood(self):
        """Test symmetries of log-likelihood."""

        @hk.without_apply_rng
        @hk.transform_with_state
        def joint_log_likelihood(x_observed):
            model = build_multinomial_network(is_training=False)
            if hk.running_init():
                # Initialise states with ancestral samples.
                model.init(x_observed)
            return model.joint_log_prob(x_observed)

        # Arbitrary input data to test on.
        x_observed = random.randint(
            next(self.key_seq), shape=(m_samples, n_features), minval=0, maxval=10
        )
        params, state = joint_log_likelihood.init(next(self.key_seq), x_observed)
        log_prob, state = joint_log_likelihood.apply(params, state, x_observed)

        # Test latent state permutation invariance of log-likelihood.
        state_permuted = state.copy()
        params_permuted = params.copy()

        # Permute latent states of the top layer.
        params_permuted["multinomial_belief/~/cap_layer"]["r"] = jnp.roll(
            params["multinomial_belief/~/cap_layer"]["r"], 1, axis=0
        )
        state_permuted["multinomial_belief/~/cap_layer"]["theta"] = jnp.roll(
            state["multinomial_belief/~/cap_layer"]["theta"], 1, axis=1
        )
        # Permute latent states of the bottom layer.
        state_permuted["multinomial_belief/~/dirichlet_layer"]["theta"] = jnp.roll(
            state["multinomial_belief/~/dirichlet_layer"]["theta"], 1, axis=1
        )
        # Permute phi two times, since layer 1 and layer 2 are both permuted.
        params_permuted["multinomial_belief/~/dirichlet_layer"]["phi"] = jnp.roll(
            jnp.roll(
                params["multinomial_belief/~/dirichlet_layer"]["phi"],
                1,
                axis=0,
            ),
            1,
            axis=1,
        )
        params_permuted["multinomial_belief/~/multinomial_layer"]["phi"] = jnp.roll(
            params["multinomial_belief/~/multinomial_layer"]["phi"],
            1,
            axis=0,
        )
        log_prob_permuted, _ = joint_log_likelihood.apply(
            params, state_permuted, x_observed
        )

        self.assertTrue(jnp.allclose(log_prob, log_prob_permuted))

    def test_calibration_without_observations(self):
        """Test posterior sampler in absence of data -> recovers prior trivially."""

        def assert_and_summarise_state_fn(state):
            bottom_layer = state["multinomial_belief/~/multinomial_layer"]
            mid_layer = state["multinomial_belief/~/dirichlet_layer"]
            cap_layer = state["multinomial_belief/~/cap_layer"]

            phi_1_squared = jnp.sum(bottom_layer["phi"] ** 2, axis=-2)
            entropy_phi_2 = jnp.sum(entropy(mid_layer["phi"], axis=-1), axis=-1)

            summary = {
                "cap_layer": {
                    "c": cap_layer["c"],
                    "entropy(r)": entropy(cap_layer["r"], axis=-1),
                },
                "mid_layer": {
                    "c": mid_layer["c"],
                    "sum_k entropy[phi_2(k)]": entropy_phi_2,
                },
                "bottom_layer": {
                    "|phi^2|": phi_1_squared,
                },
            }
            return summary

        # Close over number of samples in the init and apply functions of the forward
        # sampler.
        forward_empty_fn = hk.TransformedWithState(
            init=partial(forward_mult_dir_net.init, num_samples=0),
            apply=partial(forward_mult_dir_net.apply, num_samples=0),
        )

        histogram = simulation_based_calibration(
            forward_fn=forward_empty_fn,
            posterior_fn=mult_dir_net_sampler,
            state_fn=assert_and_summarise_state_fn,
            key=next(self.key_seq),
            n_replicates=480,
            n_posterior_samples=12,
        )

        # Test all parameters that don't have a sample index. These should coincide with
        # the prior, exactly.
        hist_c = histogram["cap_layer"]["c"]
        alpha = min(self.false_positive_rate, 0.01)
        with self.subTest(layer="cap", variable="c"):
            self.assertUniform(hist_c, alpha, name="cap_c")

        alpha = min(self.false_positive_rate, 0.01)
        hist_entr_r = histogram["cap_layer"]["entropy(r)"]
        with self.subTest(variable="Entropy[r]", layer="cap"):
            self.assertUniform(hist_entr_r, alpha=alpha, name="entropy_r")

        hist_c = histogram["mid_layer"]["c"]
        alpha = min(self.false_positive_rate, 0.01)
        with self.subTest(layer="dirichlet (middle)", variable="c"):
            self.assertUniform(hist_c, alpha, name="mid_c")

        hist_S_phi = histogram["mid_layer"]["sum_k entropy[phi_2(k)]"]
        alpha = min(self.false_positive_rate, 0.01)
        with self.subTest(
            layer="dirichlet (middle)", variable="sum_k entropy[phi_2(k)]"
        ):
            self.assertUniform(hist_S_phi, alpha=alpha, name="total_entr_mid_phi")

        n_tests = n_features
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        hist_phi_1_squared = histogram["bottom_layer"]["|phi^2|"]
        for j in range(n_features):
            with self.subTest(
                layer="multinomial (bottom)", variable="|phi^2|", feature=j
            ):
                self.assertUniform(
                    hist_phi_1_squared[..., j], alpha=alpha, name=f"bottom_phi_norm_{j}"
                )

    @skip("Skip this long failing calibration test.")
    def test_multinomial_belief_net(self):
        """Test posterior sampler of multinomial belief network."""
        n_chains = jax.local_device_count()
        self.assertGreater(n_chains, 1)

        def assert_and_summarise_state_fn(state):
            bottom_layer = state["multinomial_belief/~/multinomial_layer"]
            mid_layer = state["multinomial_belief/~/dirichlet_layer"]
            cap_layer = state["multinomial_belief/~/cap_layer"]
            theta_2 = cap_layer["theta"]
            theta_1 = mid_layer["theta"]

            mid_a = cap_layer["theta"] @ mid_layer["phi"]
            bottom_a = mid_layer["theta"] @ bottom_layer["phi"]

            phi_1_squared = jnp.sum(bottom_layer["phi"] ** 2, axis=-2)
            entropy_phi_2 = jnp.sum(entropy(mid_layer["phi"], axis=-1), axis=-1)

            # Test normalisation.
            np.testing.assert_array_almost_equal(np.sum(mid_a, axis=-1), 1.0)
            np.testing.assert_array_almost_equal(np.sum(bottom_a, axis=-1), 1.0)

            summary = {
                "cap_layer": {
                    "c": cap_layer["c"],
                    "entropy(r)": entropy(cap_layer["r"], axis=-1),
                    "entropy(theta_2)": entropy(theta_2, axis=-1),
                },
                "mid_layer": {
                    "c": mid_layer["c"],
                    "entropy(theta_1)": entropy(theta_1, axis=-1),
                    "sum_k entropy[phi_2(k)]": entropy_phi_2,
                    "entropy(a)": entropy(mid_a, axis=-1),
                },
                "bottom_layer": {
                    "|phi^2|": phi_1_squared,
                    "entropy(a)": entropy(bottom_a, axis=-1),
                },
            }
            return summary

        histogram = simulation_based_calibration(
            forward_fn=forward_mult_dir_net,
            posterior_fn=mult_dir_net_sampler,
            state_fn=assert_and_summarise_state_fn,
            key=next(self.key_seq),
            n_replicates=480,
            n_posterior_samples=12,
        )

        hist_c = histogram["cap_layer"]["c"]
        alpha = min(self.false_positive_rate, 0.01)
        with self.subTest(layer="cap", variable="c"):
            self.assertUniform(hist_c, alpha, name="cap_c")

        alpha = min(self.false_positive_rate, 0.01)
        hist_entr_r = histogram["cap_layer"]["entropy(r)"]
        with self.subTest(variable="Entropy[r]", layer="cap"):
            self.assertUniform(hist_entr_r, alpha=alpha, name="entropy_r")

        n_tests = m_samples
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        hist_S_theta_2 = histogram["cap_layer"]["entropy(theta_2)"]
        for i in range(m_samples):
            with self.subTest(variable="entropy[theta(i)]", sample=i, layer="cap"):
                self.assertUniform(
                    hist_S_theta_2[..., i], alpha=alpha, name=f"cap_entr_theta_{i}"
                )

        hist_c = histogram["mid_layer"]["c"]
        alpha = min(self.false_positive_rate, 0.01)
        with self.subTest(layer="dirichlet (middle)", variable="c"):
            self.assertUniform(hist_c, alpha, name="mid_c")

        n_tests = m_samples
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        hist_S_theta_1 = histogram["mid_layer"]["entropy(theta_1)"]
        for i in range(m_samples):
            with self.subTest(variable="entropy[theta(i)]", sample=i, layer="middle"):
                self.assertUniform(
                    hist_S_theta_1[..., i], alpha=alpha, name=f"mid_entr_theta_{i}"
                )

        hist_S_phi = histogram["mid_layer"]["sum_k entropy[phi_2(k)]"]
        alpha = min(self.false_positive_rate, 0.01)
        with self.subTest(
            layer="dirichlet (middle)", variable="sum_k entropy[phi_2(k)]"
        ):
            self.assertUniform(hist_S_phi, alpha=alpha, name="total_entr_mid_phi")

        n_tests = m_samples
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        hist_entr_2 = histogram["mid_layer"]["entropy(a)"]
        for i in range(m_samples):
            with self.subTest(variable="Entropy[activation]", sample=i, layer="middle"):
                self.assertUniform(
                    hist_entr_2[..., i], alpha=alpha, name=f"mid_entr_activ_{i}"
                )

        n_tests = n_features
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        hist_phi_1_squared = histogram["bottom_layer"]["|phi^2|"]
        for j in range(n_features):
            with self.subTest(
                layer="multinomial (bottom)", variable="|phi^2|", feature=j
            ):
                self.assertUniform(
                    hist_phi_1_squared[..., j], alpha=alpha, name=f"bottom_phi_norm_{j}"
                )

        n_tests = m_samples
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        hist_entr_1 = histogram["bottom_layer"]["entropy(a)"]
        for i in range(m_samples):
            with self.subTest(variable="Entropy[activation]", sample=i, layer="bottom"):
                self.assertUniform(
                    hist_entr_1[..., i], alpha=alpha, name=f"bottom_entr_activ_{i}"
                )
