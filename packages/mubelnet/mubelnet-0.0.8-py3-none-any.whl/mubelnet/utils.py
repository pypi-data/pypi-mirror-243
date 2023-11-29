from copy import deepcopy
from functools import partial
import re
from typing import Literal, Sequence

import haiku as hk
import jax.numpy as jnp
from jaxtyping import UInt, Array, Float, Scalar, PyTree
import numpy as np
from sklearn.metrics import silhouette_score  # type: ignore
from scipy.optimize import linear_sum_assignment  # type: ignore
from scipy.spatial.distance import cdist, pdist, squareform  # type: ignore
from scipy.stats import binom  # type: ignore


def freeze_trainable_states(
    train_states: PyTree, variable_names: Sequence[str] | None = None
) -> tuple[PyTree, PyTree]:
    """Lift out "training-mode" states to `params`.

    Args:
        train_states: States (pytree) of a model during training mode
            (i.e., `is_training=True`).
        variable_names: Names of variables to lift out of states.

    Returns:
        A pytree pair (params, states) with the frozen states moved to params.
    """
    states = deepcopy(train_states)
    if variable_names is None:
        variable_names = ("phi", "r")
        # For the Poisson gamma bel-net `c` is a local parameter,
        # while for the Multinomial bel-net c is a global parameter.
        if any(map(lambda x: "multinomial" in x, states.keys())):
            variable_names += ("c",)

    params: dict = {}
    for layer_name, layer_params in states.items():
        if layer_name not in params and any(
            map(lambda x: x in layer_params.keys(), variable_names)
        ):
            params[layer_name] = {}
        for name in variable_names:
            if name in layer_params.keys():
                params[layer_name][name] = layer_params.pop(name)
    return params, states


def is_uniform(histogram, n_replicates, alpha: float = 0.1) -> bool:
    """Determine if histogram generated from `n_replicates` is uniformly distributed.

    Args:
        alpha: Probability of false positive.
    """
    # Since the histogram is supposed to be uniform, the count in each bucket is
    # binomially distributed.
    n_bins = len(histogram)
    kwargs = {"n": n_replicates, "p": 1 / n_bins}

    # We divide by the number of bins because one bin (by accident) may be out of the
    # bands.
    q_value = alpha / n_bins
    y_lower = binom.ppf(q=q_value / 2, **kwargs)
    y_upper = binom.ppf(q=1.0 - q_value / 2, **kwargs)

    # Validate that the counts in the binds all fall within the 1-alpha % expected
    # variation around uniform distribution.
    in_bands = (histogram < y_upper) & (histogram > y_lower)
    return all(in_bands)


def to_snake_string(camel_case: str) -> str:
    """Convert a camel case string to snake case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_case).lower()


def _as_categories(x_multinomial: UInt[Array, "features"]) -> UInt[Array, "draws"]:
    """Convert multinomial sample to long vector of categorical draws."""
    #  Line up all draws in one long vector (of size `n_samples`), indicating which
    # feature was drawn.
    # Use Numpy instead of JAX implementation because it is faster.
    return np.repeat(np.arange(len(x_multinomial)), x_multinomial)  # type: ignore


def _as_multinomial(
    x_categorical: UInt[Array, "draws"], n_features: int
) -> UInt[Array, "features"]:
    """Convert string of categorical draws to multinomial representation."""
    x_test = jnp.zeros(n_features)
    x_test = x_test.at[x_categorical].add(1)  # type: ignore
    return x_test  # type: ignore


def _single_multinomial_train_test_split(
    key, x_i: UInt[Array, "features"], test_size: float = 0.2
) -> tuple[UInt[Array, "features"], UInt[Array, "features"]]:
    """Make train-test split for a single multinomial draw.

    Args:
        key: Pseudo random number generator key.
        x_i: A single multinomial observation.
        test_size: Proportion of draws for test set.
    """
    x_i = x_i.astype(int)
    n_samples = x_i.sum()
    n_test = int(n_samples * test_size)
    x_draws = _as_categories(x_i)
    # Take out `n_test` draws for test set (i.e., without replacement).
    # TODO: Put back the JAX implementation when it no longer has a memory leak.
    # x_test_draws = random.choice(key, x_draws, shape=[n_test], replace=False)
    prng = np.random.RandomState(key[0])
    x_test_draws = prng.choice(x_draws, size=[n_test], replace=False)
    # Go back to multinomial representation.
    x_test = _as_multinomial(x_test_draws, n_features=len(x_i))  # type: ignore
    # Remainder is train set.
    x_train = x_i - x_test
    return x_train, x_test


def holdout_split(key, X, test_size=0.5):
    """Make train-test split of a dataset of multinomial draws.

    Args:
        key: Pseudo random number generator key.
        X: A dataset of multinomial observations along the rows.
        test_size: Proportion of draws for test set.

    Returns:
        A pair `X_train`, `X_test` both with same shape as `X`.
    """
    key_seq = hk.PRNGSequence(key)
    _single_split = partial(_single_multinomial_train_test_split, test_size=test_size)
    x_as = []
    x_bs = []
    for x_i in X:
        x_a, x_b = _single_split(next(key_seq), x_i)
        x_as.append(x_a)
        x_bs.append(x_b)
    return jnp.stack(x_as), jnp.stack(x_bs)


def perplexity(
    X: UInt[Array, "batch features"], probs: UInt[Array, "batch features"]
) -> Float[Scalar, ""]:
    r"""Per word perplexity.
    $$
    \mathcal{L} = \exp\left(-\frac{1}{m}\sum_{i=1}^m  \sum_{j=1}^n \frac{x_{ij}
    \log p_{ij}}{\sum_{j=1}^n x_{ij}}\right)
    $$
    """
    n_words = X.sum(axis=1, keepdims=True)
    log_probs = jnp.log(probs)
    # Make sure we don't end up with nan because -inf * 0 = nan.
    log_probs = jnp.where(jnp.isneginf(log_probs) & (X == 0.0), 0.0, log_probs)
    log_likel = X * log_probs
    return jnp.exp(-jnp.mean(jnp.sum(log_likel / n_words, axis=1)))


def get_model_name(
    state: PyTree,
) -> Literal["poisson_gamma_belief", "multinomial_belief"]:
    """Is state from a poisson_gamma_belief or multinomial_belief net?"""
    return tuple(state.keys())[0].split("/~/")[0]


def get_layer_name(
    layer: Literal["bottom", "middle"],
    model_name: Literal["poisson_gamma_belief", "multinomial_belief"],
) -> str:
    naming_conventions = {
        "poisson_gamma_belief": {"bottom": "poisson_layer", "middle": "gamma_layer"},
        "multinomial_belief": {
            "bottom": "multinomial_layer",
            "middle": "dirichlet_layer",
        },
    }
    return naming_conventions[model_name][layer]


def get_hidden_unit_sizes(state: PyTree) -> tuple[int, ...]:
    """Infer the network sizes based on the state."""
    hidden_units = []
    model_name = get_model_name(state)
    bottom_layer = get_layer_name("bottom", model_name)
    for key, layer in state.items():
        if key.endswith(bottom_layer):
            continue
        hidden_units.append(layer["theta"].shape[-1])
    return tuple(hidden_units)  # type: ignore


def migrate_v005_to_v006(state: PyTree) -> PyTree:
    """Migrate theta cache name from v0.0.5 to v0.0.6."""
    model_name = get_model_name(state)
    bottom = get_layer_name("bottom", model_name)
    new_state = deepcopy(state)
    for layer_key, layer in state.items():
        if layer_key.endswith(bottom):
            if "theta" in layer:
                new_state[layer_key]["copy[theta(1)]"] = new_state[layer_key].pop(
                    "theta"
                )
        elif "theta_tplus1" in layer:
            new_state[layer_key]["copy[theta(t+1)]"] = new_state[layer_key].pop(
                "theta_tplus1"
            )
    return new_state


def _assign_clusters(topic_distr, centeroids, metric):
    n_chains = topic_distr.shape[0]
    n_topics = topic_distr.shape[1]
    # For each topic in each chain, find the best matching centroid.
    cluster_assignments = np.zeros([n_chains, n_topics], dtype=int)
    for k in range(n_chains):
        cost_matrix = cdist(centeroids, topic_distr[k], metric=metric)
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        cluster_assignments[k, col_ind] = row_ind

    return cluster_assignments


def _invert_cluster_mapping(cluster_assignments):
    n_chains = cluster_assignments.shape[0]
    n_topics = cluster_assignments.shape[1]
    # Invert cluster assignment mappings.
    cluster_assignments_inv = np.zeros_like(cluster_assignments)
    for k in range(n_topics):
        for j in range(n_chains):
            cluster_assignments_inv[j, int(cluster_assignments[j, k])] = k
    return cluster_assignments_inv


def _update_clusters(topic_distr, cluster_assignments):
    n_chains = topic_distr.shape[0]
    n_topics = topic_distr.shape[1]

    cluster_assignments_inv = _invert_cluster_mapping(cluster_assignments)
    # Per cluster, update the centroid as the centre of mass across the chains.
    centeroids = np.zeros(topic_distr.shape[1:])
    for k in range(n_topics):
        for j in range(n_chains):
            idx_c_k = cluster_assignments_inv[j, k]
            centeroids[k] += topic_distr[j, idx_c_k]
        centeroids[k] /= n_chains

    return centeroids


def cluster_latent_components(
    weights, n_iterations: int = 11, metric_name="jensenshannon", verbose=False
):
    r"""Centroid cluster the components/topics using Hungarian algorithm.

    Args:
        weights: Per chain (leading axis), the components \( \pmb{W}_k \) (second axis)
            to cluster.
        n_iterations: Number of iterations to run the clustering algorithm.

    Returns: A pair of
        cluster_assignments: Per chain (leading axis), the cluster assignments (second
            axis).
        centeroids: The centre of mass of the clusters.
    """
    # Restart the clustering algorithm with different chain centroids
    n_chains = n_restarts = weights.shape[0]
    n_topics = weights.shape[1]

    best_score = -1
    for i in range(n_restarts):
        # Restart clustering algorithm with centroid initially at the i-th chain.
        centeroids = weights[i]

        for _ in range(n_iterations):
            # 1) Assignment step.
            cluster_assignments = _assign_clusters(weights, centeroids, metric_name)

            # 2) Update step.
            centeroids = _update_clusters(weights, cluster_assignments)

            # 3) Compute pairwise distances per chain.
            x_flat = weights.reshape([n_chains * n_topics, -1])
            distances = pdist(x_flat, metric=metric_name)
            X_dist = squareform(distances)
            ss = silhouette_score(
                X_dist, cluster_assignments.flatten(), metric="precomputed"
            )

            if verbose:
                print("Silhouette score:", ss)
        if verbose:
            print("-------------------")
            print(f"Final silhouette score {i}:", ss)
        if ss > best_score:
            best_score = ss
            best_cluster_assignments = cluster_assignments
            best_centeroids = centeroids
    if verbose:
        print("Best score:", best_score)
    return best_cluster_assignments, best_centeroids
