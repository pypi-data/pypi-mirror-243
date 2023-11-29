from functools import partial

# Run the following before any XLA modules such as JAX:
import chex
from jax.config import config

config.update("jax_debug_nans", True)
chex.set_n_cpu_devices(6)


from scipy.stats import entropy
import haiku as hk
import jax
from jax import random, tree_map
import jax.numpy as jnp
from numpy.testing import assert_array_almost_equal
import numpy as np

from mubelnet.calibration import simulation_based_calibration
from mubelnet.layers import Sequential
from mubelnet.multinomial import MultinomialLayer, DirichletLayer, CapLayer
from mubelnet.sugar import scannable

from test import TestCase

from tensorflow_probability.substrates import jax as tfp  # type: ignore

m_samples = 19
n_features = 5
n_components = 3


@hk.transform_with_state
def forward(theta, is_training: bool = True):
    layer = MultinomialLayer(n_components, n_features, is_training=is_training)
    return layer.forward(theta)


@hk.transform_with_state
def step(x_ip, theta, is_training: bool = True):
    """Advance Markov chain by one step."""
    layer = MultinomialLayer(n_components, n_features, is_training=is_training)
    layer.upward(x_ip)
    layer.downward(theta)


class TestMultinomialLayer(TestCase):
    """Test sampling consistency Poisson layer."""

    def setUp(self):
        """Initialise hyperparameters."""
        self.key_seq = hk.PRNGSequence(42)
        p = 1 / 3
        scale = p / (1.0 - p)
        r = 2
        self.theta = (
            random.gamma(next(self.key_seq), r, shape=[m_samples, n_components]) * scale
        )

        # Initialise state of model.
        self.params_init, self.state_init = forward.init(next(self.key_seq), self.theta)

        # Arbitrary input data to test on.
        n_total_trials = jnp.arange(m_samples, dtype=float)

        rate = self.theta @ np.ones(shape=[n_components, n_features]) / n_features
        self.x_observed = tfp.distributions.Multinomial(n_total_trials, rate).sample(
            seed=next(self.key_seq)
        )

    def test_sample_phi(self):
        """Test tensor shape and normalisation of phi."""
        # Test shape of phi from one Gibbs step.
        _, state = step.apply(
            self.params_init,
            self.state_init,
            next(self.key_seq),
            self.x_observed,
            self.theta,
        )

        self.assertEqual(
            state["multinomial_layer"]["phi"].shape,
            (n_components, n_features),
        )
        assert_array_almost_equal(
            state["multinomial_layer"]["phi"].sum(axis=1), jnp.ones(n_components)
        )

    def test_simulation_based_calibration(self):
        """Test posterior and forward sampler using simulation based calibration."""

        @hk.transform_with_state
        def _forward():
            """Forward with theta embedded in the model for `simulation_based_calibration`."""
            layer = MultinomialLayer(n_components, n_features)
            return layer.forward(self.theta)

        _step = scannable(step)

        @partial(jax.vmap, in_axes=(0, None))
        def _gibbs_sampler(key, X_train):
            """Take a single sample after `n_burnin` steps."""
            n_burnin: int = 50

            # But change the phi, since SBC tests its consistency with the forward
            # sampler.
            key, sub_key = random.split(key)
            alpha = jnp.full(shape=(1, n_features), fill_value=5, dtype=float)
            phi = random.dirichlet(
                sub_key,
                alpha=alpha,
                shape=[n_components],
            )
            self.state_init["multinomial_layer"]["phi"] = phi

            # A for-loop (from 0,..,`n_burnin`) that runs `step`.
            carry_init = (None, self.state_init, key, X_train, self.theta)
            carry, _ = jax.lax.scan(_step, carry_init, None, length=n_burnin)

            # Return the state of the Markov chain.
            _, state_sample, _, _, _ = carry
            return state_sample

        def gibbs_sampler(key, X_train, n_samples):
            keys = random.split(key, num=n_samples)
            states = _gibbs_sampler(keys, X_train)
            # simulation_based_calibration expects two leading sample shapes (instead of
            # one) from the posterior function: n_chains x n_samples_per_chain.
            states = tree_map(lambda x: x[:, jnp.newaxis, ...], states)
            return states

        histogram = simulation_based_calibration(
            forward_fn=_forward,
            posterior_fn=gibbs_sampler,
            key=next(self.key_seq),
            n_replicates=self.n_replicates,
            n_posterior_samples=12,
        )

        # This test may fail by chance even if it is correctly implemented. Given that
        # the implementation is correct, we are willing to accept a failing unit test
        # with 10 % probability.
        n_tests = n_components * n_features

        # Test ranking uniformity of phi_kj for each channel k and feature j.
        alpha = self.false_positive_rate / n_tests
        histogram_phi = histogram["multinomial_layer"]["phi"]
        for k in range(n_components):
            for j in range(n_features):
                with self.subTest(channel=k, feature=j):
                    self.assertUniform(histogram_phi[..., k, j], alpha)


m_samples_1l, n_features_1l, n_channels_1l = 11, 5, 3


def build_shallow_model():
    # An `activation = theta @ phi` below numerical precision eps (= zero) is problematic
    # with a multinomial distribution.
    #
    # Example:
    # x ~ multinomial[0, < eps, 0,.., 0] samples uniform `x` instead of
    # x=[0, 1, 0,..,0].
    #
    # To prevent situations like this we set gamma_0 > n_channels_1l so that the
    # shape > 1 of `r_v`. This ensures that theta repels zero
    # => activation = theta @ phi is never zero.
    gamma_0 = n_channels_1l + 0.1
    return Sequential(
        layers=[
            CapLayer(n_channels_1l, gamma_0=gamma_0, e_0=gamma_0),
            MultinomialLayer(n_channels_1l, n_features_1l),
        ]
    )


@hk.transform_with_state
def forward_one_layer():
    model = build_shallow_model()
    return model.forward(m_samples=m_samples_1l)


@hk.transform_with_state
def step_one_layer(x_ip):
    """Advance Markov chain by one step."""
    model = build_shallow_model()
    model(x_ip)


def leapfrog(carry, n_steps: int):
    """A for-loop (from 0,..,`n_steps-1`) that runs `step`."""
    carry_out, _ = jax.lax.scan(scannable(step_one_layer), carry, None, length=n_steps)
    state = carry_out[1]
    return carry_out, state


@partial(jax.pmap, in_axes=(0, None, None), static_broadcasted_argnums=2)
def _gibbs_sampler(key, X_train, n_samples: int):
    """After `n_burnin` steps, take `n_samples` after `n_leap_size` steps each."""
    n_burnin: int = 3_000
    n_leap_size: int = 1_000

    # Initialise Markov chain using a forward sample state.
    sub_key, key = random.split(key)
    param_init, state_init = forward_one_layer.init(sub_key)

    # But change the phi, since SBC tests its consistency with the forward
    # sampler.
    sub_key, key = random.split(key)
    wrong_alpha = jnp.full(shape=(1, n_features_1l), fill_value=2, dtype=float)
    phi = random.dirichlet(
        sub_key,
        alpha=wrong_alpha,
        shape=[n_channels_1l],
    )
    state_init["multinomial_layer"]["phi"] = phi

    # And similarly for `r`.
    sub_key, key = random.split(key)
    wrong_gamma_0 = jnp.full(
        shape=[n_channels_1l], fill_value=n_channels_1l + 1.0, dtype=float
    )
    r = random.dirichlet(sub_key, alpha=wrong_gamma_0)
    state_init["cap_layer"]["r"] = r

    # And also for `c`.
    sub_key, key = random.split(key)
    c = random.gamma(sub_key, a=2.0)
    state_init["cap_layer"]["c"] = c

    # Collect a sample (n_samples in total) after the following number of Gibbs steps:
    # n_burnin, n_leap_size, ..., n_leapsize.
    n_steps = [n_burnin] + [n_leap_size] * (n_samples - 1)

    states = []
    sub_key, key = random.split(key)
    carry = (param_init, state_init, sub_key, X_train)
    for n in n_steps:
        carry, state_n = leapfrog(carry, n_steps=n)
        states.append(state_n)

    stacked_states = tree_map(lambda *leaves: jnp.stack(leaves), *states)
    return stacked_states


def gibbs_sampler(key, X_train, n_samples):
    n_chains = jax.local_device_count()
    n_samples_per_chain = n_samples // n_chains
    keys = random.split(key, num=n_chains)
    states = _gibbs_sampler(keys, X_train, n_samples_per_chain)
    return states


class TestOneLayerMultinomial(TestCase):
    def setUp(self):
        self.key_seq = hk.PRNGSequence(42)

    def test_shape(self):
        """Test shapes for multinomial cap-layer."""
        params, state = forward_one_layer.init(next(self.key_seq))
        x, state = forward_one_layer.apply(params, state, next(self.key_seq))

        self.assertEqual(
            state["cap_layer"]["theta"].shape,
            (m_samples_1l, n_channels_1l),
        )
        self.assertEqual(state["cap_layer"]["r"].shape, (n_channels_1l,))
        self.assertEqual(state["cap_layer"]["c"].shape, ())

        self.assertEqual(x.shape, (m_samples_1l, n_features_1l))

    def test_joint_log_likelihood(self):
        """Test symmetries of the joint likelihood."""

        @hk.without_apply_rng
        @hk.transform_with_state
        def joint_log_likelihood(x):
            model = build_shallow_model()
            if hk.running_init():
                model.init(x)
            return model.joint_log_prob(x)

        # Arbitrary input data to test on.
        x_observed = random.randint(
            next(self.key_seq), shape=(m_samples_1l, n_features_1l), minval=0, maxval=10
        )

        params, state = joint_log_likelihood.init(next(self.key_seq), x_observed)
        log_prob, state = joint_log_likelihood.apply(params, state, x_observed)

        # Test that the log-likelihood is a scalar.
        self.assertEqual(log_prob.shape, ())

        # Test latent state permutation invariance of log-likelihood.
        state_permuted = state.copy()
        state_permuted["cap_layer"]["r"] = jnp.roll(state["cap_layer"]["r"], 1, axis=0)
        state_permuted["cap_layer"]["theta"] = jnp.roll(
            state["cap_layer"]["theta"], 1, axis=1
        )
        state_permuted["multinomial_layer"]["phi"] = jnp.roll(
            state["multinomial_layer"]["phi"], 1, axis=0
        )
        log_prob_permuted, _ = joint_log_likelihood.apply(
            params, state_permuted, x_observed
        )

        self.assertTrue(jnp.allclose(log_prob, log_prob_permuted))

    def test_log_prob(self):
        """Test that log_prob doesn't depend on all parameters."""

        @hk.without_apply_rng
        @hk.transform_with_state
        def log_likehood(x):
            model = build_shallow_model()
            return model.log_prob(x)

        params, state = forward_one_layer.init(next(self.key_seq))
        # Arbitrary input data to test on.
        x_observed = random.randint(
            next(self.key_seq), shape=(m_samples_1l, n_features_1l), minval=0, maxval=10
        )

        # Test that the log-likelihood is per sample.
        log_prob, state = log_likehood.apply(params, state, x_observed)
        self.assertEqual(log_prob.shape, (m_samples_1l,))

        # Test that log_prob is independent of `c` `r`.
        state_perturbed = state.copy()
        state_perturbed["cap_layer"]["r"] = state["cap_layer"]["r"] * 10.0
        state_perturbed["cap_layer"]["c"] = state["cap_layer"]["c"] * 10.0

        # And invariant under permutation of latent state.
        # N.B.: The `theta` from `multinomial_layer` is a cached version of  the layer
        # above (in this case `theta` in `cap_layer`). So we only need to update the
        # cache.
        state_perturbed["multinomial_layer"]["copy[theta(1)]"] = jnp.roll(
            state["cap_layer"]["theta"], 1, axis=1
        )
        state_perturbed["multinomial_layer"]["phi"] = jnp.roll(
            state["multinomial_layer"]["phi"], 1, axis=0
        )
        log_prob_perturbed, _ = log_likehood.apply(params, state_perturbed, x_observed)

        self.assertTrue(jnp.allclose(log_prob, log_prob_perturbed))

    def test_sbc(self):
        """Test model using simulation based calibration."""

        def state_summary_fn(state):
            bottom_layer = state["multinomial_layer"]
            cap_layer = state["cap_layer"]
            a_1 = cap_layer["theta"] @ bottom_layer["phi"]
            theta_sqrd = jnp.sum(cap_layer["theta"] ** 2, axis=-1)
            phi_squared = jnp.sum(bottom_layer["phi"] ** 2, axis=-2)

            summary = {
                "cap_layer": {
                    "c": cap_layer["c"],
                    "entropy(r)": entropy(cap_layer["r"], axis=-1),
                    "theta^2": theta_sqrd,
                },
                "bottom_layer": {
                    "entropy": entropy(a_1, axis=-1),
                    "|phi^2|": phi_squared,
                },
            }
            return summary

        histogram = simulation_based_calibration(
            forward_fn=forward_one_layer,
            posterior_fn=gibbs_sampler,
            key=next(self.key_seq),
            state_fn=state_summary_fn,
            n_replicates=self.n_replicates,
            n_posterior_samples=12,
        )

        # This test may fail by chance even if it is correctly implemented. Given that
        # the implementation is correct, we are willing to accept a failing unit test
        # with 10 % probability.
        n_tests = n_features_1l
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        # Test ranking uniformity of phi_kj for each channel k and feature j.
        hist_phi_squared = histogram["bottom_layer"]["|phi^2|"]
        for j in range(n_features_1l):
            with self.subTest(variable="|phi^2|", feature=j, layer="bottom"):
                self.assertUniform(
                    hist_phi_squared[..., j], alpha, name=f"bottom_phi__j{j}"
                )

        hist_c = histogram["cap_layer"]["c"]
        alpha = min(self.false_positive_rate, 0.01)
        with self.subTest(layer="cap", variable="c"):
            self.assertUniform(hist_c, alpha=alpha, name="cap_c")

        n_tests = m_samples_1l
        hist_entropy = histogram["bottom_layer"]["entropy"]
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        for i in range(m_samples_1l):
            with self.subTest(variable="Entropy[activation]", sample=i, layer="bottom"):
                self.assertUniform(
                    hist_entropy[..., i], alpha=alpha, name=f"entropy_activation_{i}"
                )

        alpha = min(self.false_positive_rate, 0.01)
        hist_entr_r = histogram["cap_layer"]["entropy(r)"]
        with self.subTest(variable="entropy(r)", layer="cap"):
            self.assertUniform(hist_entr_r, alpha)

        alpha = min(self.false_positive_rate / m_samples_1l, 0.01)
        for i in range(m_samples_1l):
            with self.subTest(variable="|theta^2|", layer="cap", sample=i):
                self.assertUniform(
                    histogram["cap_layer"]["theta^2"][..., i],
                    alpha,
                    name=f"cap_norm_theta_{i}",
                )


# Network configuration.
m_samples = 11
n_features = 5
n_components1 = 3
n_components2 = 2

_, local_key = random.split(random.PRNGKey(42))

r = jnp.arange(n_components2).reshape(1, -1) + n_components2 + 0.1
theta_2 = random.dirichlet(local_key, r, shape=(m_samples,))


@hk.transform_with_state
def forward_mult_dir():
    layer1 = MultinomialLayer(n_components1, n_features)
    layer2 = DirichletLayer(n_components2, n_components1)
    return layer1.forward(layer2.forward(theta_2))


@hk.transform_with_state
def step_mult_dir(x_ip):
    layer1 = MultinomialLayer(n_components1, n_features)
    layer2 = DirichletLayer(n_components2, n_components1)
    layer2.upward(*layer1.upward(x_ip))
    layer1.downward(*layer2.downward(theta_2))


def leapfrog_mult_dir(carry, n_steps: int):
    """A for-loop (from 0,..,`n_steps-1`) that runs `step`."""
    carry_out, _ = jax.lax.scan(scannable(step_mult_dir), carry, None, length=n_steps)
    state = carry_out[1]
    return carry_out, state


@partial(jax.pmap, in_axes=(0, None, None), static_broadcasted_argnums=2)
def _mult_dir_gibbs_sampler(key, X_train, n_samples: int):
    """After `n_burnin` steps, take `n_samples` after `n_leap_size` steps each."""
    n_burnin: int = 200
    n_leap_size: int = 50

    # Initialise Markov chains using a forward sample state.
    key, sub_key = random.split(key)
    _, state_init = forward_mult_dir.init(sub_key)

    # return stacked_states
    n_steps = [n_burnin] + [n_leap_size] * (n_samples - 1)

    states = []
    key, sub_key = random.split(key)
    carry = (None, state_init, sub_key, X_train)
    for n in n_steps:
        carry, state_n = leapfrog_mult_dir(carry, n_steps=n)
        states.append(state_n)

    stacked_states = tree_map(lambda *leaves: jnp.stack(leaves), *states)
    return stacked_states


def mult_dir_gibbs_sampler(key, X_train, n_samples):
    n_chains = jax.local_device_count()
    n_samples_per_chain = n_samples // n_chains
    keys = random.split(key, num=n_chains)
    states = _mult_dir_gibbs_sampler(keys, X_train, n_samples_per_chain)
    return states


class TestDirichletLayer(TestCase):
    """Test the middle Dirichlet layer with the observed multinomial layer."""

    def setUp(self):
        self.key_seq = hk.PRNGSequence(42)
        # Simulation based calibration settings.
        self.probability_false_negative = 0.1

    @hk.testing.transform_and_run
    def test_shape(self):
        """Test shapes of `theta`, and `x`."""
        layer1 = MultinomialLayer(n_components1, n_features)
        layer2 = DirichletLayer(n_components2, n_components1)
        theta_1 = layer2.forward(theta_2)
        x_forward = layer1.forward(theta_1)
        self.assertEqual(theta_1.shape, (m_samples, n_components1))
        self.assertEqual(x_forward.shape, (m_samples, n_features))

    @hk.testing.transform_and_run
    def test_normalisation(self):
        """Test that `theta` is normalised."""
        layer2 = DirichletLayer(n_components2, n_components1)
        theta_1 = layer2.forward(theta_2)
        assert_array_almost_equal(theta_1.sum(axis=1), 1.0)

    def test_simulation_based_calibration(self):
        """Test posterior samples using simulation based calibration."""

        def summarise_fn(state):
            bottom_layer = state["multinomial_layer"]
            middle_layer = state["dirichlet_layer"]
            activation = middle_layer["theta"] @ bottom_layer["phi"]
            activation = activation + 1.1754944e-38

            phi_squared = jnp.sum(middle_layer["phi"] ** 2, axis=[-2, -1])
            summary = {
                "middle_layer": {
                    "c": middle_layer["c"],
                    "|phi^2|": phi_squared,
                },
                "bottom_layer": {
                    "entropy": entropy(activation, axis=-1),
                },
            }
            return summary

        histogram = simulation_based_calibration(
            forward_fn=forward_mult_dir,
            posterior_fn=mult_dir_gibbs_sampler,
            state_fn=summarise_fn,
            key=next(self.key_seq),
            n_replicates=self.n_replicates,
            n_posterior_samples=12,
        )

        hist_c = histogram["middle_layer"]["c"]
        alpha = 0.01
        with self.subTest(variable="c"):
            self.assertUniform(hist_c, alpha=alpha, name="c")

        hist_squared = histogram["middle_layer"]["|phi^2|"]
        alpha = 0.01
        with self.subTest(variable="|phi^2|", layer=2):
            self.assertUniform(hist_squared, alpha, name="norm_phi")

        hist_theta = histogram["bottom_layer"]["entropy"]
        n_tests = m_samples
        alpha = min(self.probability_false_negative / n_tests, 0.01)
        for i in range(m_samples):
            with self.subTest(sample=i, variable="entropy", layer=1):
                self.assertUniform(hist_theta[..., i], alpha, name=f"entropy_theta_{i}")


@hk.transform_with_state
def frozen_kernel():
    model = Sequential(
        layers=[
            CapLayer(n_components2),
            DirichletLayer(n_components2, n_components1),
            MultinomialLayer(n_components1, n_features),
        ],
        name="two_layer_net",
        is_training=False,
    )
    x = model.forward(m_samples=5)
    model(x)


class TestFrozen(chex.TestCase):
    """Test variables can be clamped."""

    def setUp(self):
        self.key = random.PRNGKey(42)

    def test_cap_params(self):
        """Test that frozen CapLayer parameter end up in params."""
        key, sub_key = random.split(self.key)
        params, state = frozen_kernel.init(sub_key)

        _, state = frozen_kernel.apply(params, state, key)
        self.assertIn("r", params["cap_layer"])
        self.assertIn("c", params["cap_layer"])
        self.assertNotIn("theta", params["cap_layer"])
        self.assertNotIn("r", state["cap_layer"])
        self.assertNotIn("c", state["cap_layer"])
        self.assertIn("theta", state["cap_layer"])

    def test_multinomial_params(self):
        """Test that frozen MultinomialLayer parameters end up in params"""
        key, rng_sub = random.split(self.key)
        params, state = frozen_kernel.init(rng_sub)

        _, state = frozen_kernel.apply(params, state, key)
        self.assertIn("phi", params["multinomial_layer"])
        self.assertNotIn("phi", state["multinomial_layer"])

    def test_dirichlet_params(self):
        """Test that frozen DirichletLayer parameters end up in params."""
        key, sub_key = random.split(self.key)
        params, state = frozen_kernel.init(sub_key)

        _, state = frozen_kernel.apply(params, state, key)
        self.assertIn("phi", params["dirichlet_layer"])
        self.assertIn("c", params["dirichlet_layer"])
        self.assertNotIn("theta", params["dirichlet_layer"])

        self.assertNotIn("phi", state["dirichlet_layer"])
        self.assertNotIn("c", state["dirichlet_layer"])
        self.assertIn("theta", state["dirichlet_layer"])
