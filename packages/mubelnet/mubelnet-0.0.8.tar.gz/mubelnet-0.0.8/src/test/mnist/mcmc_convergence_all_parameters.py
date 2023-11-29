import sys

# Add end-to-end package to path.
import sys
from pathlib import Path

sys.path.append(str(Path("../../").absolute()))

from io import BytesIO
import os
from pathlib import Path
import pickle
import sys

# Run the following before any XLA modules such as JAX:
import chex

chex.set_n_cpu_devices(4)

import haiku as hk
import jax
from jax import random
import jax.numpy as jnp
from matplotlib import pyplot as plt
import numpy as np
from sklearn import datasets
import tensorflow as tf

# Import the remaining JAX related
from gabenet.mcmc import sample_markov_chain
from gabenet.nets import MultinomialDirichletBelieve


# Pseudo-random number generator sequence.
key_seq = hk.PRNGSequence(42)

digits = datasets.load_digits()
n_samples = len(digits.images)
X_train = digits.images.reshape((n_samples, -1))
m_samples, n_features = X_train.shape


def plot_to_tensor(figure):
    """Convert matplotlib figure to tensor flow image."""
    # Save the plot to a PNG in memory.
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(figure)
    buf.seek(0)
    # Convert PNG buffer to TF image
    image = tf.image.decode_png(buf.getvalue(), channels=4)
    # Add the batch dimension
    return tf.expand_dims(image, 0)


def plot_convergence_2d(states):
    f = plt.figure()
    for i in range(n_chains):
        plt.plot(states[i, :, 0], states[i, :, 1], "-o", label=f"chain: {i}")
    plt.legend()
    return f


def plot_convergence_1d(states):
    f = plt.figure()
    for i in range(n_chains):
        plt.plot(np.arange(states[i].shape[0]), states[i], label=f"chain {i}")
    plt.legend()
    return f


def plot_convergence_3d(states):
    n_chains, n_draws, _, n_channels = states.shape
    imgs = []
    for k in range(n_channels):
        f = plt.figure()
        for i in range(n_chains):
            plt.plot(np.arange(n_draws), states[i, :, 0, k], "-o", label=f"chain: {i}")
        plt.xlabel("Sample")
        plt.ylabel(f"phi(k={k})")
        plt.ylim([0, 1])
        plt.legend()
        f_tensor = plot_to_tensor(f)
        imgs.append(tf.squeeze(f_tensor))
    return imgs


def plots_to_tensorboard(states, writer, i):
    with writer.as_default():
        r_states = states["multinomial_dirichlet_believe/~/multinomial_cap_layer"]["r"]
        f_r = plot_convergence_2d(r_states)
        tf.summary.image("r", plot_to_tensor(f_r), step=i)

        c = states["multinomial_dirichlet_believe/~/dirichlet_layer"]["c"]
        f_c = plot_convergence_1d(c)
        tf.summary.image("c", plot_to_tensor(f_c), step=i)

        phi_2 = states["multinomial_dirichlet_believe/~/dirichlet_layer"]["phi"]
        phi_panels = plot_convergence_3d(phi_2)
        tf.summary.image(
            "phi_2",
            phi_panels,
            step=i,
            max_outputs=10,
        )
        writer.flush()


log_dir = sys.argv[1] if len(sys.argv) > 1 else os.environ["TENSORBOARD_LOG"]
TENSORBOARD_LOG = Path(log_dir)
N_LOOPS = int(os.environ.get("N_LOOPS", 15))
TENSORBOARD_LOG.mkdir(parents=True, exist_ok=True)

print("Writing checkpoints and tensorboards to", TENSORBOARD_LOG)
writer = tf.summary.create_file_writer(str(TENSORBOARD_LOG))


def build_gamma_belief_net():
    """A two-layer decoder network."""
    n_hidden_units = (2, 10)
    return MultinomialDirichletBelieve(n_hidden_units, n_features, gamma_0=3.0)


@hk.transform_with_state
def kernel():
    """Advances the Markov chain by one step."""
    model = build_gamma_belief_net()
    model(X_train)


@hk.transform_with_state
def forward():
    """Initialise Markov chain using forward samples."""
    model = build_gamma_belief_net()
    return model.forward(m_samples)


n_chains = 4
key_per_chain = random.split(next(key_seq), num=n_chains)
param_init, state_init = jax.vmap(forward.init)(key_per_chain)

kernel = jax.jit(kernel.apply)


state_checkpoints = []

for i in range(N_LOOPS):
    states = sample_markov_chain(
        next(key_seq),
        n_samples=100,
        # n_samples=8,
        kernel=kernel,
        initial_params=param_init,
        initial_state=state_init,
        n_burnin_steps=0,
        n_leap_size=5,
        # n_leap_size=0,
    )

    states["multinomial_dirichlet_believe/~/multinomial_layer"][
        "phi"
    ].block_until_ready()
    print(f"Saving checkpoint {i+1}...\t", end="")
    # Last MCMC state becomes new initial state.
    state_init = jax.tree_util.tree_map(lambda x: x[:, -1, ...], states)
    with open(TENSORBOARD_LOG / f"checkpoint_{i+1}.pkl", "wb") as fo:
        pickle.dump(state_init, fo)
        print("[DONE]")
    state_checkpoints.append(states)

    # Make a plot.
    all_states = jax.tree_util.tree_map(
        lambda *args: jnp.concatenate(args, axis=1), *state_checkpoints
    )
    plots_to_tensorboard(all_states, writer, i=i + 1)


with open(TENSORBOARD_LOG / f"samples.pkl", "wb") as fo:
    pickle.dump(states, fo)
