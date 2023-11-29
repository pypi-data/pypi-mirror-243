from functools import partial
from typing import Literal

from mubelnet.nets import MultinomialBelief, PoissonGammaBelief
from mubelnet.random import PRNGSequence
from mubelnet.utils import perplexity
import haiku as hk
import jax
from jax import random
from jax.tree_util import tree_map
import jax.numpy as jnp

from dataset import load_digits
from train_utils import TrainState, save_states, load_last_checkpoint


# Training hyperparameters
RANDOM_SEED = 42
N_BURNIN = 100_000
LOG_EVERY = 100
N_SAMPLES = 1_280 * 4
key_seq = PRNGSequence(jax.random.PRNGKey(RANDOM_SEED))

# Print out training hyperparameters for logging.
print(f"RANDOM_SEED = {RANDOM_SEED}")
print(f"N_BURNIN = {N_BURNIN}")
print(f"N_SAMPLES = {N_SAMPLES}")

# Model hyperparameters.
MODEL: Literal["multinomial_belief", "poisson_gamma_belief"] = "multinomial_belief"
n_topics = 10
HIDDEN_LAYER_SIZES = (n_topics, n_topics, n_topics)
GAMMA_0 = 1.0
ETA = 0.05
_bottom_layer_name = (
    f"{MODEL}/~/multinomial_layer"
    if MODEL == "multinomial_belief"
    else f"{MODEL}/~/poisson_layer"
)
# Print out model hyperparameters for logging.
print(f"MODEL = {MODEL}")
print(f"n_topics = {n_topics}")
print(f"HIDDEN_LAYER_SIZES = {HIDDEN_LAYER_SIZES}")
print(f"GAMMA_0 = {GAMMA_0}")
print(f"ETA = {ETA}")
print(f"CHAINS = {jax.device_count()}")

n_chains = jax.device_count()

X_train, X_test = load_digits()
n_features = X_train.shape[1]


if n_chains == 1:
    print("ERROR: Only one visible device!")
    exit(1)


@hk.transform_with_state
def kernel(n_hidden_units=HIDDEN_LAYER_SIZES, X=X_train):
    """Advance the Markov chain by one step."""
    if MODEL == "multinomial_belief":
        model = MultinomialBelief(
            n_hidden_units,
            n_features,
            gamma_0=GAMMA_0,
            eta=ETA,
        )
    else:
        model = PoissonGammaBelief(
            n_hidden_units, n_features, gamma_0=GAMMA_0, eta=ETA
        )
    # Do one Gibbs sampling step.
    model(X)


def probability(params, state):
    bottom_params = params.get(_bottom_layer_name, {})
    bottom_state = state[_bottom_layer_name]
    phi = bottom_params.get("phi", bottom_state.get("phi"))
    theta = bottom_state["copy[theta(1)]"]
    probs = theta @ phi
    probs /= probs.sum(axis=-1, keepdims=True)
    return probs


def initialise(key, model, hidden_layer_sizes) -> TrainState:
    """Initialise training state."""
    key, subkey = random.split(key)
    keys = random.split(subkey, jax.device_count())
    params, state = jax.pmap(kernel.init)(keys)
    return TrainState(
        params,
        state,
        key,
        step=0,
        model_name=model,
        hidden_layer_sizes=hidden_layer_sizes,
    )


def evaluate(params, states, X, axis=[0, 1]):
    """Compute perplexity over chains and samples by default (axis=[0, 1])."""
    probs = probability(params, states).mean(axis)
    return perplexity(X, probs)


def train_step(kernel_fn, train_state: TrainState, n_steps) -> TrainState:
    """Do a set of Markov chain monte carlo steps and save checkpoint."""
    key_seq = hk.PRNGSequence(train_state.key)
    state = train_state.state
    # 1) Burn-in model.
    for i in range(n_steps):
        _, state = kernel_fn(
            train_state.params, state, random.split(next(key_seq), n_chains)
        )
        print(".", end="")

    train_state = TrainState(
        train_state.params,
        state,
        next(key_seq),
        train_state.step + n_steps,
        MODEL,
        train_state.hidden_layer_sizes,
    )
    return train_state


# When starting from scratch, initialize the Markov chain and run with burn in.
if (train_state := load_last_checkpoint(MODEL, HIDDEN_LAYER_SIZES)) is None:
    key = jax.random.PRNGKey(RANDOM_SEED)
    train_state = initialise(key, MODEL, HIDDEN_LAYER_SIZES)
    loss_test = evaluate(train_state.params, train_state.state, X_test, axis=[0])
    print("Initial perplexity on test set", loss_test)

n_start = train_state.step // LOG_EVERY
n_stop = N_BURNIN // LOG_EVERY
kernel_fn = jax.pmap(
    partial(kernel.apply, n_hidden_units=train_state.hidden_layer_sizes),
    in_axes=(None, 0, 0),
)

for _ in range(n_start, n_stop):
    train_state = train_step(kernel_fn, train_state, n_steps=LOG_EVERY)
    save_states(train_state, {})
    print("Burn in", train_state.step)

trace = []
for i in range(N_SAMPLES // n_chains):
    train_state = train_step(kernel_fn, train_state, n_steps=1)
    trace.append(train_state.state)

states = tree_map(lambda *xs: jnp.stack(xs, axis=1), *trace)

save_states(train_state, states)
