from unittest import TestCase

import haiku as hk
from jax import random
import jax.numpy as jnp
from numpy.testing import assert_array_equal

from mubelnet.utils import (
    _as_categories,
    _as_multinomial,
    _single_multinomial_train_test_split,
    holdout_split,
    perplexity,
)


class TestUtils(TestCase):
    def setUp(self):
        self.key_seq = hk.PRNGSequence(42)

    def test_as_mulitnomial_and_categories(self):
        """Test that multinomial and categorical representations are inverse."""
        n_features = 10
        x_sample = random.randint(
            next(self.key_seq), shape=[n_features], minval=0, maxval=10
        )
        x_draws = _as_categories(x_sample)
        x_test = _as_multinomial(x_draws, n_features=n_features)
        assert_array_equal(x_sample, x_test)

    def test_single_train_test_split(self):
        """Test train-test split of a single multinomial."""
        fraction = 1 / 6
        x_sample = random.randint(next(self.key_seq), shape=[10], minval=0, maxval=10)
        x_train, x_test = _single_multinomial_train_test_split(
            next(self.key_seq), x_sample, test_size=fraction
        )
        self.assertEqual(x_test.sum(), int(x_sample.sum() * fraction))
        self.assertEqual(x_train.sum() + x_test.sum(), x_sample.sum())
        assert_array_equal(x_train + x_test, x_sample)

    def test_holdout_split(self):
        """Test train-test split of a dataset of multinomials."""
        fraction = 1 / 3
        n_features = 10
        n_samples = 20
        x_sample = random.randint(
            next(self.key_seq), shape=[n_samples, n_features], minval=0, maxval=10
        )
        # Triple to take out a third (=fraction).
        x_sample = x_sample * 3
        x_train, x_test = holdout_split(
            next(self.key_seq), x_sample, test_size=fraction
        )
        self.assertEqual(x_test.sum(), int(x_sample.sum() * fraction))
        assert_array_equal(x_test.sum(axis=1), x_sample.sum(axis=1) * fraction)
        self.assertEqual(x_train.sum() + x_test.sum(), x_sample.sum())
        assert_array_equal(
            x_train.sum(axis=1) + x_test.sum(axis=1), x_sample.sum(axis=1)
        )
        assert_array_equal(x_train + x_test, x_sample)

    def test_perplexity(self):
        """Test perplexity on exactly solvable probability distributions."""
        n_features = 10
        x_sample = random.randint(
            next(self.key_seq), shape=[n_features, 3], minval=0, maxval=10
        )
        uniform_probability = jnp.full(x_sample.shape, fill_value=1 / n_features)
        self.assertAlmostEqual(
            perplexity(x_sample, uniform_probability), n_features, places=5
        )

        perfect_probability = jnp.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=float,
        )
        x_sample = perfect_probability * 10.0
        self.assertAlmostEqual(perplexity(x_sample, perfect_probability), 1)
