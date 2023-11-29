from pathlib import Path

from gabenet.utils import holdout_split
import jax
import jax.numpy as jnp
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer


_PATH = Path(__file__).parent


def load_20newsgroups(random_state=42):
    if not (_PATH / "train.npy").exists():
        files = fetch_20newsgroups(subset="all")
        cv = CountVectorizer(min_df=10, max_features=2_000)
        X = cv.fit_transform(files.data)
        X_dense = jnp.array(X.todense())
        key = jax.random.PRNGKey(random_state)
        X_train, X_test = holdout_split(key, X_dense, test_size=0.7)
        jnp.save(_PATH / "train.npy", X_train)
        jnp.save(_PATH / "test.npy", X_test)
    else:
        X_train = jnp.load(_PATH / "train.npy")
        X_test = jnp.load(_PATH / "test.npy")
    return X_train, X_test
