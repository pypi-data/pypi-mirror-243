from functools import partial
from typing import Literal, Sequence

from gabenet.mcmc import sample_markov_chain
from gabenet.nets import MultinomialDirichletBelieve, PoissonGammaBelieve
from gabenet.random import PRNGSequence
from gabenet.utils import perplexity, get_hidden_unit_sizes
import haiku as hk
import jax
from jax import random
import jax.numpy as jnp
from jaxtyping import PRNGKeyArray

from dataset import load_20newsgroups


# Training hyperparameters
RANDOM_SEED = 43
key_seq = PRNGSequence(jax.random.PRNGKey(RANDOM_SEED))

# Print out training hyperparameters for logging.
print(f"RANDOM_SEED = {RANDOM_SEED}")

# Model hyperparameters.
MODEL: Literal[
    "multinomial_dirichlet_believe", "poisson_gamma_believe"
] = "multinomial_dirichlet_believe"
n_topics = 200
HIDDEN_LAYER_SIZES = (n_topics,)
GAMMA_0 = 1.0
ETA = 0.05
_bottom_layer_name = (
    f"{MODEL}/~/multinomial_layer"
    if MODEL == "multinomial_dirichlet_believe"
    else f"{MODEL}/~/poisson_layer"
)
# Print out model hyperparameters for logging.
print(f"MODEL = {MODEL}")
print(f"n_topics = {n_topics}")
print(f"HIDDEN_LAYER_SIZES = {HIDDEN_LAYER_SIZES}")
print(f"GAMMA_0 = {GAMMA_0}")
print(f"ETA = {ETA}")

n_chains = jax.device_count()

X_train, X_test = load_20newsgroups()
n_features = X_train.shape[1]


@hk.transform_with_state
def kernel(X=X_train):
    """Advance the Markov chain by one step."""
    if MODEL == "multinomial_dirichlet_believe":
        model = MultinomialDirichletBelieve(
            HIDDEN_LAYER_SIZES,
            n_features,
            gamma_0=GAMMA_0,
            eta=ETA,
        )
    else:
        model = PoissonGammaBelieve(
            HIDDEN_LAYER_SIZES, n_features, gamma_0=GAMMA_0, eta=ETA
        )
    # Do one Gibbs sampling step.
    model(X)
