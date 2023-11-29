from unittest import TestCase

import jax
from jax import random
import jax.numpy as jnp
import numpy as np
from numpy.testing import assert_array_equal
from scipy.stats import chisquare

from mubelnet.random import PRNGSequence, augmented_poisson, augment_reduce


class TestAugmentation(TestCase):
    def setUp(self):
        """Initialise random states."""
        self.n_channels = 2
        self.n_features = 3
        self.m_samples = 5
        self.key_seq = PRNGSequence(random.PRNGKey(42))

        # Initialise phi and theta for augmentation.
        a_phi = jnp.full(self.n_features, fill_value=1.5)
        self.phi = random.dirichlet(
            next(self.key_seq), alpha=a_phi, shape=[self.n_channels]
        )
        # Large shape of gamma to ensure that > 13 observations per sample.
        a_theta = jnp.full(self.n_channels, fill_value=0.75)
        self.theta = random.dirichlet(
            next(self.key_seq), alpha=a_theta, shape=[self.m_samples]
        )

        # Initialise counts based on phi and theta.
        self.x = (
            random.poisson(next(self.key_seq), lam=5 * self.theta @ self.phi) * 1_000
        )

    def test_augmentation_count_conservation(self):
        """Test that the augmented samples sums to the original sample."""
        # Verify the input shapes of generating matrices.
        self.assertEqual(self.phi.shape, (self.n_channels, self.n_features))
        self.assertEqual(self.theta.shape, (self.m_samples, self.n_channels))

        rate = self.theta[:, jnp.newaxis, :] * self.phi.T[jnp.newaxis, ...]
        x_augmented = augmented_poisson(next(self.key_seq), rate, self.x)
        self.assertEqual(
            x_augmented.shape, (self.m_samples, self.n_features, self.n_channels)
        )
        assert_array_equal(x_augmented.sum(axis=-1), self.x)

    def test_augment_reduce(self):
        """Test that iterative `augment_reduce` equals batch computation."""
        # Ground truth: Expected counts based on multinomial distribution.
        log_rate = jnp.log(self.theta[:, jnp.newaxis, :]) + jnp.log(
            self.phi.T[jnp.newaxis, ...]
        )
        rate = jax.nn.softmax(log_rate)
        m_true = jnp.sum(rate * self.x[..., jnp.newaxis], axis=1).round()
        x_jk_true = jnp.sum(rate * self.x[..., jnp.newaxis], axis=0).round()

        batch_sizes = [4, 6]
        for b in batch_sizes:
            with self.subTest(batch_size=b):
                m_ik, x_jk = augment_reduce(
                    next(self.key_seq),
                    self.theta,
                    self.phi,
                    self.x,
                    # Dataset not divisible by batch sizes -> last batch has to be padded with
                    # zeroes.
                    mini_batch_size=b,
                )

                self.assertEqual(m_ik.shape, self.theta.shape)
                self.assertEqual(x_jk.shape, self.phi.transpose().shape)
                assert_array_equal(m_ik.sum(axis=1), self.x.sum(axis=1))
                assert_array_equal(x_jk.sum(axis=1), self.x.sum(axis=0))

                # Test that the variables are statistically indistinguishable.
                for i in range(self.m_samples):
                    res = chisquare(m_ik[i], m_true[i])
                    with self.subTest(variable="m_ik", i=i):
                        self.assertGreater(res.pvalue, 0.05)

                for j in range(self.n_features):
                    res = chisquare(x_jk[j], x_jk_true[j])
                    with self.subTest(variable="x_jk", j=j):
                        self.assertGreater(res.pvalue, 0.05)

    def test_dtype_casting(self):
        """Test that dtypes are safely cast to the correct type."""
        rate = self.theta[:, jnp.newaxis, :] * self.phi.T[jnp.newaxis, ...]
        x_augmented = augmented_poisson(
            next(self.key_seq), np.array(rate), np.array(self.x)
        )
        self.assertTrue(jnp.issubdtype(x_augmented.dtype, jnp.integer))
