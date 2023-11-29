from functools import partial
from unittest import TestCase, skip

from jax import random, vmap
from jax.scipy.special import digamma, gammaln
import jax.numpy as jnp
import numpy as np
from numpy.testing import assert_allclose
import haiku as hk

from mubelnet.calibration import simulation_based_calibration
from mubelnet.random import (
    chinese_restaurant_table,
    dirichlet_multinomial,
    posterior_gamma_chinese_restaurant_table,
)
from mubelnet.utils import is_uniform

_stirling_cache: dict[str, int] = {}


def sterling_first_kind(n: int, k: int):
    key = str(n) + "," + str(k)

    if key in _stirling_cache.keys():
        return _stirling_cache[key]
    if n == k == 0:
        return 1
    if n > 0 and k == 0:
        return 0
    if k > n:
        return 0
    result = sterling_first_kind(n - 1, k - 1) + (n - 1) * sterling_first_kind(n - 1, k)
    _stirling_cache[key] = result
    return result


def crt_probability_mass_function(l_tables, n_customers, r):
    """The probability of `l` tables given `n` customers with concentration `r`."""
    # Compute log probability first to prevent under or overflow.
    log_prob = (
        gammaln(r)
        + l_tables * jnp.log(r)
        - gammaln(n_customers + r)
        + jnp.log(jnp.abs(sterling_first_kind(n_customers, l_tables)))
    )
    return jnp.exp(log_prob)


def crt_mean(n, r):
    """The mean of the Chinese Restaurant table distribution."""
    return r * (digamma(r + n) - digamma(r))


class TestChineseRestaurantTable(TestCase):
    """Test the Chinese restaurant table sampler."""

    def setUp(self):
        self.key = random.PRNGKey(42)
        self.n_customers = jnp.array([0, 1, 10, 100, 1000])
        self.r_concentration = 10.0 ** (jnp.arange(0, 4) - 0.5)
        # Make Cartesian product of arrays: n x r.
        self.n_cross_r = jnp.array(
            jnp.meshgrid(self.n_customers, self.r_concentration)
        ).T.reshape(-1, 2)

    def test_mean_scalar(self):
        """Test that the mean is correct when sampling scalars."""
        key = self.key
        # Test the distribution's mean one configuration at a time.
        for n, r in self.n_cross_r:
            with self.subTest(n=n, r=r):
                key, sub_key = random.split(key)
                n = n.astype(int)
                # l_samples = chinese_restaurant_table2(self.key, n, r, shape=[200_000])
                l_samples = chinese_restaurant_table(sub_key, n, r, shape=[100_000])
                assert_allclose(l_samples.mean(), crt_mean(n, r), rtol=1e-2)

    def test_single_sample_vectorised(self):
        """Test that distribution is vectorisable one sample at a time."""
        n = self.n_cross_r[:, 0].astype(int).reshape(2, 5, 2)
        r = self.n_cross_r[:, 1].reshape(2, 5, 2)

        l_samples = []
        keys = random.split(self.key, num=100_000)
        for k in keys:
            l_tables = chinese_restaurant_table(k, n, r, shape=None)
            l_samples.append(l_tables)

        true_mean = crt_mean(n, r)

        assert_allclose(jnp.array(l_samples).mean(axis=0), true_mean, rtol=1e-2)

    def test_mean_vectorised(self):
        """Test that we can random distribution is vectorisable."""
        # Unravel product into array.
        n = self.n_cross_r[:, 0].astype(int)
        r = self.n_cross_r[:, 1]
        l_samples = chinese_restaurant_table(
            self.key,
            n,
            r,
            shape=[100_000, 1],
        )
        true_mean = crt_mean(n, r)
        assert_allclose(l_samples.mean(axis=0), true_mean, rtol=1e-2)

        n = self.n_cross_r[:, 0].astype(int).reshape(2, 5, 2)
        r = self.n_cross_r[:, 1].reshape(2, 5, 2)
        l_samples = chinese_restaurant_table(
            self.key,
            n,
            r,
            shape=[5, 20_000, 1, 1, 1],
        )
        true_mean = crt_mean(n, r)
        assert_allclose(l_samples.mean(axis=[0, 1]), true_mean, rtol=1e-2)

    def test_mean_vectorised_broadcast(self):
        """Test summary statistics of vectorised implementation with broadcasting."""
        ls = []
        n = self.n_customers[None, ...]
        r = self.r_concentration[..., None]
        keys = random.split(self.key, num=10_000)
        for k in keys:
            l_samples = chinese_restaurant_table(k, n, r)
            ls.append(l_samples)
        true_mean = crt_mean(n, r)
        assert_allclose(np.mean(ls, axis=0), true_mean, rtol=1e-2)


class TestDirMult(TestCase):
    def setUp(self):
        self.key = random.PRNGKey(42)
        self.n_flat = 2 ** jnp.arange(0, 5)
        self.alpha_flat = jnp.array(
            [
                [0.8, 0.1, 0.1],
                [5.0, 10.0, 10.0],
                [5.0, 5.0, 5.0],
                [0.3, 5.0, 0.6],
            ]
        )

        n = []
        a = []
        for n_i in self.n_flat:
            for a_i in self.alpha_flat:
                n.append(n_i)
                a.append(a_i)
        self.n_trials = jnp.array(n)
        self.alpha = jnp.array(a).reshape(self.n_trials.shape + (3,))

    def test_shape(self):
        """Test that the samples have the correct shape."""
        # Generate single sample for each element.
        x = dirichlet_multinomial(self.key, self.n_trials, self.alpha)
        self.assertEqual(x.shape, self.alpha.shape)

        # For each parameter, generate 5 samples.
        y = dirichlet_multinomial(
            self.key, self.n_trials, self.alpha, shape=(5, len(self.n_trials))
        )
        self.assertEqual(y.shape, (5,) + self.alpha.shape)

    @skip("Crash on 64bit")
    def test_mean(self):
        """Test covergence of samples to mean."""

        def true_dir_mult_mean(n_trials, alpha):
            """Analytical expression of mean of DirMult distribution."""
            return n_trials.reshape(-1, 1) * alpha / alpha.sum(axis=-1, keepdims=True)

        x = dirichlet_multinomial(
            self.key, self.n_trials, self.alpha, shape=(750_000, len(self.n_trials))
        )
        assert_allclose(
            x.mean(axis=0), true_dir_mult_mean(self.n_trials, self.alpha), rtol=1e-2
        )

    def test_broadcast(self):
        """Test broadcasting of arrays with unequal shape."""
        n_trials = self.n_flat.reshape(-1, 1)
        alpha = self.alpha_flat[jnp.newaxis, ...]
        x = dirichlet_multinomial(self.key, n_trials, alpha)
        self.assertEqual(x.shape, (5, 4, 3))

        # Verify that this broadcasting does not result in copies of the variables.
        m_samples = 100
        y = dirichlet_multinomial(self.key, n_trials, alpha, shape=(m_samples, 5, 4))

        # When they are copies, the sum should equal m_samples times the first element.
        self.assertEqual(y.shape, (m_samples, 5, 4, 3))
        # When they are not copies, the probability is small if the Dirichlet's are not
        # sparse.
        duplicates = m_samples * y[0] == y.sum(axis=0)
        self.assertFalse(jnp.any(duplicates))

    def test_dtype_casting(self):
        """Test that dtypes are safely cast to the correct type."""
        n_trials = self.n_flat.reshape(-1, 1)
        alpha = self.alpha_flat[jnp.newaxis, ...]

        x_dirmult = dirichlet_multinomial(self.key, np.array(n_trials), np.array(alpha))
        self.assertEqual(x_dirmult.dtype, jnp.uint32)


class TestPosteriorGammaCRT(TestCase):
    def test_return_scalar(self):
        """Test that a scalar is returned."""
        m = jnp.array([1, 2, 2])
        n = jnp.array([3, 5, 7])
        alpha0 = posterior_gamma_chinese_restaurant_table(
            key=random.PRNGKey(42), m=m, n=n, a=1, b=1
        )
        self.assertEqual(np.shape(alpha0), ())

    def test_simulation_based_calibration(self):
        """Use simulation based calibration to check posterior."""
        a = 1.0
        b = 1.0
        n = jnp.array([3, 5, 7, 9, 11])

        @hk.transform_with_state
        def forward():
            """Samples from Chinese restaurant table with gamma concentration."""
            key = hk.next_rng_key()
            alpha_0 = random.gamma(key, a) / b
            hk.set_state("alpha_0", alpha_0)

            key = hk.next_rng_key()
            concentration = jnp.full_like(n, alpha_0, dtype=alpha_0.dtype)
            m = chinese_restaurant_table(key, n, concentration, shape=n.shape)
            return m

        def gibbs(key, m_observed, n_samples):
            keys = random.split(key, num=n_samples)
            posterior_fn = partial(
                posterior_gamma_chinese_restaurant_table, m=m_observed, n=n, a=a, b=b
            )
            alpha = vmap(posterior_fn)(keys)
            # Simulation based calibration expects the leading axis to refer to the
            # chain. So let's add it.
            return {"~": {"alpha_0": alpha[jnp.newaxis, ...]}}

        histogram = simulation_based_calibration(
            forward, gibbs, random.PRNGKey(42), n_replicates=200
        )
        alpha_0 = histogram["~"]["alpha_0"]
        self.assertTrue(is_uniform(alpha_0, n_replicates=200, alpha=0.05))
