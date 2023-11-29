from io import BytesIO
from matplotlib import pyplot as plt
import numpy as np
import tensorflow as tf


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


def plot_convergence_2d(states, n_chains=4):
    f = plt.figure()
    for i in range(n_chains):
        plt.plot(states[i, :, 0], states[i, :, 1], "-o", label=f"chain: {i}")
    plt.legend()
    return f


def plot_convergence_1d(states, n_chains=4):
    f = plt.figure()
    for i in range(n_chains):
        plt.plot(np.arange(states[i].shape[0]), states[i], label=f"chain {i}")
    plt.legend()
    return f


def plots_to_tensorboard(states, writer, i):
    with writer.as_default():
        r_states = states["multinomial_dirichlet_believe/~/cap_layer"]["r"]
        f_r = plot_convergence_2d(r_states)
        tf.summary.image("r", plot_to_tensor(f_r), step=i)

        c = states["multinomial_dirichlet_believe/~/dirichlet_layer"]["c"]
        f_c = plot_convergence_1d(c)
        tf.summary.image("c", plot_to_tensor(f_c), step=i)
        writer.flush()
