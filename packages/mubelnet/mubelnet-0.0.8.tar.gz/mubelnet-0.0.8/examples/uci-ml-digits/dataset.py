from jax import random
from sklearn import datasets
from mubelnet.utils import holdout_split


def load_digits(random_state: int = 43):
    digits = datasets.load_digits()
    n_samples = len(digits.images)
    X = digits.images.reshape((n_samples, -1))
    X_train, X_test = holdout_split(random.PRNGKey(random_state), X)
    return X_train, X_test
