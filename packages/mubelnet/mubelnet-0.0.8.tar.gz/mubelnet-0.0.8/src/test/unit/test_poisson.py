from functools import partial

# Run the following before any XLA modules such as JAX:
import chex

chex.set_n_cpu_devices(6)


import haiku as hk
import jax
from jax import random, tree_map
import jax.numpy as jnp
from scipy.stats import entropy
from numpy.testing import assert_array_almost_equal

from mubelnet.calibration import simulation_based_calibration
from mubelnet.layers import Sequential
from mubelnet.poisson import CapLayer, GammaLayer, PoissonLayer
from mubelnet.sugar import scannable

from test import TestCase

m_samples = 5
n_features = 3
n_components = 2


def build_shallow_model(is_training: bool = True):
    return Sequential(
        layers=[
            CapLayer(n_components),
            PoissonLayer(n_components, n_features),
        ],
        name="gamma_belief_network",
        is_training=is_training,
    )


@hk.transform_with_state
@chex.assert_max_traces(1)
def forward(is_training: bool = True):
    model = build_shallow_model(is_training)
    return model.forward(m_samples)


@hk.transform_with_state
@chex.assert_max_traces(2)
def step(x_ip, is_training: bool = True):
    """Advance Markov chain by one step."""
    model = build_shallow_model(is_training)
    return model(x_ip)


def leapfrog(carry, n_steps: int):
    """A for-loop (from 0,..,`n_steps-1`) that runs `step`."""
    carry_out, _ = jax.lax.scan(scannable(step), carry, None, length=n_steps)
    state = carry_out[1]
    return carry_out, state


@partial(jax.pmap, in_axes=(0, None, None), static_broadcasted_argnums=2)
def _gibbs_sampler(key, X_train, n_samples: int):
    """After `n_burnin` steps, take `n_samples` after `n_leap_size` steps each."""
    n_burnin: int = 3_000
    n_leap_size: int = 2_000

    # Initialise Markov chain using a forward sample state.
    sub_key, key = random.split(key)
    _, state_init = forward.init(sub_key)

    # Collect a sample (n_samples in total) after the following number of Gibbs steps:
    # n_burnin, n_leap_size, ..., n_leapsize.
    n_steps = [n_burnin] + [n_leap_size] * (n_samples - 1)

    states = []
    sub_key, key = random.split(key)
    carry = (None, state_init, sub_key, X_train)
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


class TestPoissonCap(TestCase):
    """Test a model composed of a Poisson and cap layer."""

    def setUp(self):
        super().setUp()
        self.key_seq = hk.PRNGSequence(42)
        self.n_replicates = 480

    def test_log_likelihood_cap(self):
        """Test the log-likelihood of the cap layer."""

        @hk.without_apply_rng
        @hk.transform_with_state
        def log_likelihood(x):
            """A shallow network with mixed params and state."""
            model = Sequential(
                layers=[
                    CapLayer(n_components, frozen="r"),
                    PoissonLayer(n_components, n_features),
                ],
                name="gamma_belief_network",
            )
            if hk.running_init():
                model.init(x)
            return model.joint_log_prob(x)

        # Arbitrary input data to test on.
        x_observed = random.randint(
            next(self.key_seq), shape=(m_samples, n_features), minval=0, maxval=10
        )
        params, state = log_likelihood.init(next(self.key_seq), x_observed)

        log_prob, state = log_likelihood.apply(params, state, x_observed)

        # Test that the log-likelihood is a scalar.
        self.assertEqual(log_prob.shape, ())

        # Test latent state permutation invariance of log-likelihood.
        state_permuted = state.copy()
        params_permuted = params.copy()
        params_permuted["cap_layer"]["r"] = jnp.roll(
            params["cap_layer"]["r"], 1, axis=0
        )
        state_permuted["cap_layer"]["theta"] = jnp.roll(
            state["cap_layer"]["theta"], 1, axis=1
        )
        state_permuted["poisson_layer"]["phi"] = jnp.roll(
            state["poisson_layer"]["phi"], 1, axis=0
        )
        log_prob_permuted, _ = log_likelihood.apply(
            params_permuted, state_permuted, x_observed
        )

        self.assertTrue(jnp.allclose(log_prob, log_prob_permuted))

    def test_training_mode(self):
        """Test setting training and inference mode."""
        # Test that trainable parameters are in state but not in params.
        params, state = forward.init(next(self.key_seq), is_training=True)
        self.assertIn("r", state["cap_layer"])
        self.assertIn("phi", state["poisson_layer"])
        self.assertNotIn("r", params.get("cap_layer", {}))
        self.assertNotIn("phi", params.get("poisson_layer", {}))

        # Test that frozen parameters are in params but not in state.
        params, state = forward.init(next(self.key_seq), is_training=False)
        self.assertIn("r", params["cap_layer"])
        self.assertIn("phi", params["poisson_layer"])
        self.assertNotIn("r", state.get("cap_layer", {}))
        self.assertNotIn("phi", state.get("poisson_layer", {}))

    def test_simulation_based_calibration(self):
        """Test posterior sampling using simulation based calibration."""

        def summarise_fn(state):
            bottom_layer = state["poisson_layer"]
            cap_layer = state["cap_layer"]
            activation = cap_layer["theta"] @ bottom_layer["phi"]
            theta_sum = jnp.sum(cap_layer["theta"], axis=-1)
            phi_squared = jnp.sum(bottom_layer["phi"] ** 2, axis=-2)

            r_norm = cap_layer["r"].sum(axis=-1, keepdims=True)
            entropy_r = entropy(cap_layer["r"] / r_norm, axis=-1)

            summary = {
                "cap_layer": {
                    "c": cap_layer["c"],
                    "|r|": r_norm,
                    "entropy(r)": entropy_r,
                    "|theta|": theta_sum,
                },
                "bottom_layer": {
                    "activation": activation,
                    "phi_squared": phi_squared,
                },
            }
            return summary

        histogram = simulation_based_calibration(
            forward_fn=forward,
            posterior_fn=gibbs_sampler,
            state_fn=summarise_fn,
            key=next(self.key_seq),
            n_replicates=self.n_replicates,
            n_posterior_samples=12,
        )

        # This test may fail by chance even if it is correctly implemented. Given that
        # the implementation is correct, we are willing to accept a failing unit test
        # with 10 % probability.
        n_tests = n_features
        alpha = self.false_positive_rate / n_tests
        # Test ranking uniformity of phi_kj for each channel k and feature j.
        hist_phi = histogram["bottom_layer"]["phi_squared"]
        for j in range(n_features):
            with self.subTest(variable="sum_k phi(k,j)^2", feature=j):
                self.assertUniform(hist_phi[..., j], alpha=alpha, name=f"phi_{j}")

        n_tests = 1
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        with self.subTest(variable="|r|"):
            self.assertUniform(histogram["cap_layer"]["|r|"], alpha=alpha, name="|r|")

        n_tests = 1
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        hist_r_entr = histogram["cap_layer"]["entropy(r)"]
        with self.subTest(variable="entropy(r)"):
            self.assertUniform(hist_r_entr, alpha=alpha, name="entropy_r")

        n_tests = m_samples * n_features
        alpha = self.false_positive_rate / n_tests
        hist_activation = histogram["bottom_layer"]["activation"]
        for i in range(m_samples):
            for j in range(n_features):
                with self.subTest(variable="activation(1)", sample=i, feature=j):
                    self.assertUniform(
                        hist_activation[..., i, j],
                        alpha=alpha,
                        name=f"activation__{i}_{j}",
                    )

        # Test ranking uniformity of phi_kj for each channel k and feature j.
        n_tests = m_samples
        hist_c = histogram["cap_layer"]["c"]
        for i in range(m_samples):
            with self.subTest(variable="c", sample=i):
                self.assertUniform(
                    hist_c[..., i],
                    alpha=self.false_positive_rate / n_tests,
                    name=f"c_{i}",
                )

        alpha = min(self.false_positive_rate / m_samples, 0.01)
        for i in range(m_samples):
            with self.subTest(variable="|theta|", i=i):
                self.assertUniform(
                    histogram["cap_layer"]["|theta|"][..., i],
                    alpha,
                    name=f"norm_theta_{i}",
                )


m_samples_poisson = 25
n_features_poisson = 3
n_components_poisson = 2


@hk.transform_with_state
def poisson_forward(theta, is_training: bool = True):
    layer = PoissonLayer(
        n_components_poisson, n_features_poisson, is_training=is_training
    )
    return layer.forward(theta)


@hk.transform_with_state
def poisson_step(x_ip, theta, is_training: bool = True):
    """Advance Markov chain by one step."""
    layer = PoissonLayer(
        n_components_poisson, n_features_poisson, is_training=is_training
    )
    layer.upward(x_ip)
    layer.downward(theta)


class TestPoissonLayer(TestCase):
    """Test sampling consistency Poisson layer."""

    def setUp(self):
        """Initialise hyperparameters."""
        self.key, sub_key = random.split(random.PRNGKey(42))
        p = 1 / 3
        scale = p / (1.0 - p)
        r = 2
        self.theta = (
            random.gamma(sub_key, r, shape=[m_samples_poisson, n_components_poisson])
            * scale
        )

        # Arbitrary input data to test on.
        self.key, sub_key = random.split(self.key)
        self.x_observed = random.randint(
            sub_key, shape=(m_samples_poisson, n_features_poisson), minval=0, maxval=10
        )

        # Initialise state of model.
        self.key, sub_key = random.split(self.key)
        self.params_init, self.state_init = poisson_forward.init(sub_key, self.theta)

    def test_permutation_symmetry_log_likelihood(self):
        """Test log likelihood is invariant under latent state permutations."""

        @hk.without_apply_rng
        @hk.transform_with_state
        def log_likelihood(x_ip, theta):
            """Advance Markov chain by one step."""
            layer = PoissonLayer(n_components_poisson, n_features_poisson)
            return layer.joint_log_prob(theta, x_ip)

        ll, state = log_likelihood.apply(
            self.params_init, self.state_init, self.x_observed, self.theta
        )
        # Log-likelihood returns a scalar.
        self.assertEqual(len(ll.shape), 0)

        # The log-likelihood is invariant under permutations of the latent states.
        state_permuted = state.copy()
        theta_permuted = jnp.roll(self.theta, 1, axis=1)
        state_permuted["poisson_layer"]["phi"] = jnp.roll(
            state_permuted["poisson_layer"]["phi"], 1, axis=0
        )

        ll_permuted, _ = log_likelihood.apply(
            self.params_init, state_permuted, self.x_observed, theta_permuted
        )
        self.assertAlmostEqual(ll, ll_permuted, places=5)

    def test_training_mode(self):
        """Test setting training and inference mode."""
        self.key, key = random.split(self.key)

        # Test that trainable parameters are in state but not in params.
        params, state = poisson_forward.init(self.key, self.theta, is_training=True)

        _, state = poisson_step.apply(
            params, state, key, self.x_observed, self.theta, is_training=True
        )
        self.assertIn("phi", state["poisson_layer"])
        self.assertNotIn("phi", params.get("poisson_layer", {}))

        # Test that frozen parameters are in params but not in state.
        params, state = poisson_forward.init(self.key, self.theta, is_training=False)
        _, state = poisson_step.apply(
            params, state, key, self.x_observed, self.theta, is_training=False
        )
        self.assertIn("phi", params["poisson_layer"])
        self.assertNotIn("phi", state.get("poisson_layer", {}))

    def test_sample_phi(self):
        """Test tensor shape and normalisation of phi."""
        # Test shape of phi from one Gibbs step.
        self.key, key = random.split(self.key)
        _, state = poisson_step.apply(
            self.params_init, self.state_init, key, self.x_observed, self.theta
        )

        self.assertEqual(
            state["poisson_layer"]["phi"].shape,
            (n_components_poisson, n_features_poisson),
        )
        assert_array_almost_equal(
            state["poisson_layer"]["phi"].sum(axis=1), jnp.ones(n_components_poisson)
        )

    def test_simulation_based_calibration(self):
        """Test posterior and forward sampler using simulation based calibration."""

        @hk.transform_with_state
        def forward():
            """Forward with theta embedded in the model for `simulation_based_calibration`."""
            layer = PoissonLayer(n_components_poisson, n_features_poisson)
            return layer.forward(self.theta)

        @partial(jax.vmap, in_axes=(0, None))
        @jax.jit
        def _gibbs_sampler(key, X_train):
            """Take a single sample after `n_burnin` steps."""
            n_burnin: int = 100

            # But change the phi, since SBC tests its consistency with the forward
            # sampler.
            sub_key, key = random.split(key)
            alpha = jnp.full(shape=(1, n_features_poisson), fill_value=5, dtype=float)
            phi = random.dirichlet(
                sub_key,
                alpha=alpha,
                shape=[n_components_poisson],
            )
            self.state_init["poisson_layer"]["phi"] = phi

            # A for-loop (from 0,..,`n_burnin`) that runs `step`.
            carry_init = (None, self.state_init, key, X_train, self.theta)
            carry, _ = jax.lax.scan(
                scannable(poisson_step), carry_init, None, length=n_burnin
            )

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
            forward_fn=forward,
            posterior_fn=gibbs_sampler,
            key=self.key,
            n_replicates=self.n_replicates,
            n_posterior_samples=12,
        )

        # This test may fail by chance even if it is correctly implemented. Given that
        # the implementation is correct, we are willing to accept a failing unit test
        # with 10 % probability.
        n_tests = n_components_poisson * n_features_poisson
        alpha = self.false_positive_rate / n_tests

        # Test ranking uniformity of phi_kj for each channel k and feature j.
        histogram_phi = histogram["poisson_layer"]["phi"]
        for k in range(n_components_poisson):
            for j in range(n_features_poisson):
                with self.subTest(channel=k, feature=j):
                    self.assertUniform(
                        histogram_phi[..., k, j], alpha, name=f"phi__k{k}_j{j}"
                    )


# Network configuration.
m_samples = 11
n_features = 5
n_components1 = 3
n_components2 = 1

_, local_key = random.split(random.PRNGKey(42))

r = jnp.arange(n_components2).reshape(1, -1) + 2
scale = jnp.arange(m_samples).reshape(-1, 1) + 0.5
theta = random.gamma(local_key, r, shape=(m_samples, n_components2)) * scale


@hk.transform_with_state
@chex.assert_max_traces(1)
def forward_poisson_gamma():
    layer1 = PoissonLayer(n_components1, n_features)
    layer2 = GammaLayer(n_components2, n_components1)
    return layer1.forward(layer2.forward(theta))


@hk.transform_with_state
@chex.assert_max_traces(2)
def step_poisson_gamma(x_ip):
    layer1 = PoissonLayer(n_components1, n_features)
    layer2 = GammaLayer(n_components2, n_components1)
    layer2.upward(*layer1.upward(x_ip))
    layer1.downward(*layer2.downward(theta))


def leapfrog_poisson_gamma(carry, n_steps: int):
    """A for-loop (from 0,..,`n_steps-1`) that runs `step`."""
    carry_out, _ = jax.lax.scan(
        scannable(step_poisson_gamma), carry, None, length=n_steps
    )
    state = carry_out[1]
    return carry_out, state


@partial(jax.pmap, in_axes=(0, 0, None, None), static_broadcasted_argnums=3)
def _poisson_gamma_gibbs_sampler(state_init, key, X_train, n_samples: int):
    """After `n_burnin` steps, take `n_samples` after `n_leap_size` steps each."""
    n_burnin: int = 500
    n_leap_size: int = 250

    # Collect a sample (n_samples in total) after the following number of Gibbs steps:
    # n_burnin, n_leap_size, ..., n_leapsize.
    carry = (None, state_init, key, X_train)
    carry, _ = leapfrog_poisson_gamma(carry, n_steps=n_burnin - n_leap_size)
    carry, stacked_states = jax.lax.scan(
        lambda c, _: leapfrog_poisson_gamma(c, n_leap_size),
        carry,
        xs=None,
        length=n_samples,
    )

    return stacked_states


def poisson_gamma_gibbs_sampler(key, X_train, n_samples):
    n_chains = jax.local_device_count()

    if n_chains == 1:
        raise ValueError("Error: only one device available. Reconfigure XLA_FLAGS.")

    if n_samples % n_chains > 0:
        raise ValueError(
            "Number of samples {n_samples} not divisible by number of devices {n_chains}."
        )

    n_samples_per_chain = n_samples // n_chains

    # Initialise Markov chains using a forward sample state.
    key, sub_key = random.split(key)
    _, state_init = forward_poisson_gamma.init(sub_key)
    forward_sample = jax.pmap(forward_poisson_gamma.apply, in_axes=(None, None, 0))
    # Generate a new initial state for each chain.
    key, *sub_keys = random.split(key, num=2 * n_chains + 1)
    keys_forward, keys_backward = sub_keys[:n_chains], sub_keys[n_chains:]
    _, state_inits = forward_sample(None, state_init, jnp.array(keys_forward))

    # But change the phi, since SBC tests its consistency with the forward
    # sampler.
    sub_key, key = random.split(key)
    wrong_alpha = jnp.full(shape=(1, 1, n_components1), fill_value=2, dtype=float)
    phi = random.dirichlet(
        sub_key,
        alpha=wrong_alpha,
        shape=state_inits["gamma_layer"]["phi"].shape[:-1],
    )
    state_inits["gamma_layer"]["phi"] = phi

    # And also for `c`.
    sub_key, key = random.split(key)
    wrong_e0 = jnp.full(shape=[m_samples], fill_value=2, dtype=float)
    c = random.gamma(
        sub_key,
        a=wrong_e0,
        shape=state_inits["gamma_layer"]["c"].shape,
    )
    state_inits["gamma_layer"]["c"] = c

    states = _poisson_gamma_gibbs_sampler(
        state_inits, jnp.array(keys_backward), X_train, n_samples_per_chain
    )
    return states


class TestGammaLayer(TestCase):
    """Test the Gamma layer in conjuction with the Poisson layer."""

    def setUp(self):
        self.key_seq = hk.PRNGSequence(42)

    def test_log_likelihood(self):
        """Test log-likelihood of model."""

        @hk.without_apply_rng
        @hk.transform_with_state
        def log_likelihood_poisson_gamma(x_ip, theta):
            layer1 = PoissonLayer(n_components1, n_features)
            layer2 = GammaLayer(n_components2, n_components1)
            ll2, theta_1 = layer2.joint_log_prob(theta)
            ll1 = layer1.joint_log_prob(theta_1, x_ip)
            return ll1 + ll2

        # Initialise the states.
        params, state = forward_poisson_gamma.init(next(self.key_seq))

        # Arbitrary input data to test on.
        self.x_observed = random.randint(
            next(self.key_seq), shape=(m_samples, n_features), minval=0, maxval=10
        )

        # Compute the log-likelihood.
        log_prob, state = log_likelihood_poisson_gamma.apply(
            params, state, self.x_observed, theta
        )
        self.assertEqual(log_prob.shape, tuple())

        state_permuted = state.copy()
        theta_permuted = jnp.roll(theta, 1, axis=1)
        state_permuted["gamma_layer"]["phi"] = jnp.roll(
            state_permuted["gamma_layer"]["phi"], 1, axis=0
        )
        log_prob_permuted, _ = log_likelihood_poisson_gamma.apply(
            params, state_permuted, self.x_observed, theta_permuted
        )

        # Check that the log-likelihood is invariant under permutation of the latent state.
        self.assertTrue(jnp.allclose(log_prob, log_prob_permuted))

    def test_simulation_based_calibration(self):
        """Test posterior samples using simulation based calibration."""

        def summarise_fn(state):
            bottom_layer = state["poisson_layer"]
            middle_layer = state["gamma_layer"]
            activation = middle_layer["theta"] @ bottom_layer["phi"]
            phi_squared = jnp.sum(middle_layer["phi"] ** 2, axis=[-2, -1])
            summary = {
                "gamma_layer": {
                    "c": middle_layer["c"],
                    "|phi^2|": phi_squared,
                },
                "bottom_layer": {
                    "activation": activation,
                },
            }
            return summary

        histogram = simulation_based_calibration(
            forward_fn=forward_poisson_gamma,
            posterior_fn=poisson_gamma_gibbs_sampler,
            state_fn=summarise_fn,
            key=next(self.key_seq),
            n_replicates=self.n_replicates,
            n_posterior_samples=12,
        )

        hist_c = histogram["gamma_layer"]["c"]
        n_tests = m_samples
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        for i in range(m_samples):
            with self.subTest(sample=i):
                self.assertUniform(hist_c[..., i], alpha=alpha, name=f"c_{i}")

        n_tests = 1
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        hist_phi_square = histogram["gamma_layer"]["|phi^2|"]
        with self.subTest(variable="|phi^2|", layer=2):
            self.assertUniform(hist_phi_square, alpha=alpha, name="norm_gamma_phi")

        hist_activation = histogram["bottom_layer"]["activation"]
        n_tests = m_samples * n_features
        alpha = min(self.false_positive_rate / n_tests, 0.01)
        for i in range(m_samples):
            for j in range(n_features):
                with self.subTest(sample=i, feature=j):
                    self.assertUniform(
                        hist_activation[..., i, j],
                        alpha=alpha,
                        name=f"activation__i{i}_j{j}",
                    )


def build_frozen_cap_model():
    """Build a model with frozen r cap parameters."""
    model = Sequential(
        layers=[
            CapLayer(n_components, frozen=["r"]),
            PoissonLayer(n_components, n_features),
        ],
        name="gamma_belief_network",
    )
    return model


@hk.transform_with_state
def frozen_cap_forward():
    model = build_frozen_cap_model()
    return model.forward(m_samples)


@hk.transform_with_state
def frozen_cap_step(x_ip):
    """Advance Markov chain by one step."""
    model = build_frozen_cap_model()
    return model(x_ip)


def build_frozen_poisson_model():
    """Build a model with frozen phi poisson parameters."""
    model = Sequential(
        layers=[
            CapLayer(n_components),
            PoissonLayer(n_components, n_features, frozen=["phi"]),
        ],
        name="gamma_belief_network",
    )
    return model


@hk.transform_with_state
def frozen_poisson_forward():
    model = build_frozen_poisson_model()
    return model.forward(m_samples)


@hk.transform_with_state
def frozen_poisson_step(x_ip):
    """Advance Markov chain by one step."""
    model = build_frozen_poisson_model()
    return model(x_ip)


def build_frozen_gamma_model():
    """Build a model with frozen phi gamma parameters."""
    model = Sequential(
        layers=[
            CapLayer(n_components2),
            GammaLayer(n_components2, n_components1, frozen=["phi"]),
            PoissonLayer(n_components1, n_features),
        ],
        name="two_layer_gamma_belief_net",
    )
    return model


@hk.transform_with_state
def frozen_gamma_forward():
    model = build_frozen_gamma_model()
    return model.forward(m_samples)


@hk.transform_with_state
def frozen_gamma_step(x_ip):
    model = build_frozen_gamma_model()
    model(x_ip)


class TestFrozen(chex.TestCase):
    """Test variables can be clamped."""

    def setUp(self):
        self.key = random.PRNGKey(42)

    def test_cap_params(self):
        """Test that frozen CapLayer parameter end up in params."""
        key, rng_key = random.split(self.key)
        params, state = frozen_cap_forward.init(rng_key)

        _, state = frozen_cap_forward.apply(params, state, key)
        self.assertIn("r", params["cap_layer"])
        self.assertNotIn("c", params["cap_layer"])
        self.assertNotIn("theta", params["cap_layer"])
        self.assertNotIn("r", state["cap_layer"])
        self.assertIn("c", state["cap_layer"])
        self.assertIn("theta", state["cap_layer"])

    def test_poisson_params(self):
        """Test that frozen PoissonLayer parameters end up in params"""
        key, rng_key = random.split(self.key)
        params, state = frozen_poisson_forward.init(rng_key)

        _, state = frozen_poisson_forward.apply(params, state, key)
        self.assertIn("phi", params["poisson_layer"])
        self.assertNotIn("cap_layer", params)
        self.assertNotIn("phi", state["poisson_layer"])

    def test_gamma_params(self):
        """Test that frozen GammaLayer parameters end up in params"""
        key, rng_key = random.split(self.key)
        params, state = frozen_gamma_forward.init(rng_key)

        _, state = frozen_gamma_forward.apply(params, state, key)
        self.assertIn("phi", params["gamma_layer"])
        self.assertNotIn("c", params["gamma_layer"])
        self.assertNotIn("theta", params["gamma_layer"])
        self.assertNotIn("poisson_layer", params)
        self.assertNotIn("cap_layer", params)

        self.assertNotIn("phi", state["gamma_layer"])
        self.assertIn("c", state["gamma_layer"])
        self.assertIn("theta", state["gamma_layer"])
        self.assertIn("phi", state["poisson_layer"])
        self.assertIn("c", state["cap_layer"])

    def test_poisson_step(self):
        """Test that a step doesn't update the frozen PoissonLayer parameter."""
        key, rng_key = random.split(self.key)
        params, state = frozen_poisson_forward.init(rng_key)
        key, rng_key = random.split(key)
        X_train, state = frozen_poisson_forward.apply(params, state, rng_key)

        key, rng_key = random.split(key)

        _, state_updated = frozen_poisson_step.apply(params, state, rng_key, X_train)

        chex.assert_trees_all_equal_structs(state, state_updated)
        chex.assert_trees_all_equal_shapes(state, state_updated)

    def test_cap_step(self):
        """Test that a step doesn't update the frozen CapLayer parameter."""
        key, sub_key = random.split(self.key)
        params, state = frozen_cap_forward.init(sub_key)
        key, sub_key = random.split(key)
        X_train, state = frozen_cap_forward.apply(params, state, sub_key)

        key, sub_key = random.split(key)

        _, state_updated = frozen_cap_step.apply(params, state, sub_key, X_train)
        chex.assert_trees_all_equal_structs(state, state_updated)
        chex.assert_trees_all_equal_shapes(state, state_updated)
