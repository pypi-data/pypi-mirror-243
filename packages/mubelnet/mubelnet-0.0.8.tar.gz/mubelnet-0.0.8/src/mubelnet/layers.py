from collections.abc import Iterable
from typing import Optional

import haiku as hk
from jax import random
import jax.numpy as jnp
from tensor_annotations.axes import Batch, Channels, Features
from tensor_annotations.jax import Array2, float32, uint32

from mubelnet.random import augment_reduce
from mubelnet.utils import to_snake_string


def _sample_phi(
    x_jk: Array2[uint32, Features, Channels], dirichlet_prior: float
) -> Array2[float32, Channels, Features]:
    """Posterior phi, the latent state signature, given augmented Poisson counts.

    ϕ ~ Dir(x_.jk + eta).
    """
    p: Array2[float32, Features, Channels] = x_jk + dirichlet_prior
    phi = random.dirichlet(hk.next_rng_key(), alpha=jnp.transpose(p))  # type: ignore

    return phi  # type: ignore


class _Module(hk.Module):
    """Haiku model with option to freeze states."""

    def __init__(self, name: str, frozen: Optional[Iterable[str]] = None):
        """
        Args:
            frozen: Variables that are considered parameters of the module instead of
                states. That is, they are clamped during inference (but _not_ in the
                forward sampler).
        """
        super().__init__(name=name)
        if frozen is None:
            self.frozen: frozenset = frozenset()
        else:
            self.frozen = frozenset(frozen)
        self.frozen_ = self.frozen

    def set_training(self, is_training: bool) -> None:
        """Toggle training mode."""
        self.is_training = is_training
        # The frozen_ (a superset of `frozen`) variables are not updated during Gibbs
        # sampling.
        self.frozen_ = frozenset(self.frozen)

    def _get(self, name, shape=None, dtype=float, init=None):
        """Get state or parameter if it is frozen."""
        if name in self.frozen_:
            return hk.get_parameter(name, shape, dtype, init)
        return hk.get_state(name, shape, dtype, init)

    def _set(self, name, value):
        """Set state to its value, unless frozen."""
        if name not in self.frozen_:
            hk.set_state(name, value)
        else:

            def _initialiser(shape, dtype):
                return jnp.zeros(shape, dtype) + value

            # Set the value as initialiser for `get_parameter`.
            hk.get_parameter(name, value.shape, value.dtype, init=_initialiser)


class BaseMiddleLayer(_Module):
    r"""Common intermediate layer for the Poisson or multinomial belief net."""

    def __init__(
        self,
        input_size: int,
        output_size: int,
        name: Optional[str] = None,
        eta: float = 1.0,
        e_0: float = 1.0,
        f_0: float = 1.0,
        frozen: Optional[tuple[str]] = None,
        is_training: bool = True,
    ):
        r"""
        Args:
            input_size: The number of latent variables/topics coming into the layer.
            output_size: The number of features coming out of layer.
            name: Name of this layer.
            eta: Dirichlet hyperparameter \(\eta\) on weights.
            e_0: Shape hyperparameter of activation scale.
            f_0: Scale hyperparameter of activation scale.
            is_training: Is the model in training or inference mode?
        """
        if name is None:
            name = to_snake_string(self.__class__.__name__)
        super().__init__(name=name, frozen=frozen)
        self.input_size = output_size
        self.n_components = input_size
        self.eta = eta
        self.e_0 = e_0
        self.f_0 = f_0
        self.set_training(is_training)


class BaseObservedLayer(_Module):
    r"""Common layer for the observed Poisson and multinomial layer."""

    def __init__(
        self,
        input_size: int,
        output_size: int,
        name: Optional[str] = None,
        eta: float = 1.0,
        frozen: Optional[tuple[str]] = None,
        is_training: bool = True,
    ):
        r"""
        Args:
            input_size: The number of latent variables coming into the layer.
            output_size: The number of features in the dataset.
            name: Name of this layer.
            eta: Dirichlet hyperparameter \(\eta\) on weights.
            is_training: Whether the model is in training or inference mode.
        """
        if name is None:
            name = to_snake_string(self.__class__.__name__)

        super().__init__(name=name, frozen=frozen)
        self.output_size = output_size
        self.input_size = input_size
        self.eta = eta
        self.set_training(is_training)

    def forward_activation(
        self, theta: Array2[float32, Batch, Channels]
    ) -> Array2[float32, Batch, Features]:
        r"""Do a ancestral sampling step up to and including the activation.
        \(\{\phi_{kj}^{(1)}, a_{ij}^{(1)}\}_{i,j,k} \mid \theta_{ik}^{(1)} \)."""
        assert self.input_size == theta.shape[1]

        # Sample and save state phi.
        alpha = jnp.full(shape=(1, self.output_size), fill_value=self.eta, dtype=float)
        phi: Array2[float32, Channels, Features] = random.dirichlet(
            hk.next_rng_key(),
            alpha=alpha,
            shape=(self.input_size,),
        )  # type: ignore
        self._set("phi", phi)

        # Instead of saving rate(i,j,k) = θ(i,j)ϕ(j,k), we store θ from the layer above
        # to conserve memory.
        self._set("copy[theta(1)]", theta)

        # Sample and save sampled activation state.
        activation = theta @ phi
        return activation

    def upward(self, x: Array2[uint32, Batch, Features]):
        r"""Gibbs sample upward.

        $$
        \chi_{ijk}^{(1)}  \sim \mathrm{Mult}[x_{ij}^{(1)}, \{θ_{ik}^{(1)}ϕ_{kj}^{(1)}\}_k], \\
        \phi_{kj}^{(1)} \sim \mathrm{Dir}[\{\eta + \sum_{i} \chi_{ijk}^{(1)}\}_j],
        $$
        where by construction \(\sum_{k=1}^{K_1}\chi_{ijk}^{(1)} = x_{ij}^{(1)}\). We
        propogate the latent counts \(m_{ik}^{(1)} = \sum_{j=1}^n \chi^{(1)}_{ijk}\)
        (with \(n\) the number of features, `input_size`) and the corresponding
        rate \(q^{(1)}_i\) upwards to the layers above.

        Args:
            x: Training data, of shape `(m_samples, n_features)`, to propagate upwards.
        """
        m_samples = x.shape[0]

        # Infer `rate` from ϕ and θ from the layer above.
        theta_shape = (m_samples, self.input_size)
        phi_shape = (self.input_size, self.output_size)
        theta = self._get("copy[theta(1)]", theta_shape)
        phi = self._get("phi", phi_shape)  # type: ignore

        m_ik, x_jk = augment_reduce(hk.next_rng_key(), theta, phi, x)  # type: ignore

        if "phi" not in self.frozen_:
            phi = _sample_phi(x_jk, dirichlet_prior=self.eta)  # type: ignore
            self._set("phi", phi)

        return m_ik

    def downward(self, theta: Array2[float32, Batch, Channels]):
        # Instead of storing rate, we save θ from the layer above to conserve memory.
        # (Rate is cubic instead of quadratic in memory). We compute rate from θ and ϕ
        # when we need it.
        hk.set_state("copy[theta(1)]", theta)


class Sequential(hk.Module):
    """Sample probabilistic layers in sequence."""

    def __init__(self, layers, name: Optional[str] = None, is_training: bool = True):
        super().__init__(name=name)
        self.layers = layers
        self.set_training(is_training)

    def set_training(self, is_training: bool):
        """Toggle training mode for all layers."""
        self.is_training = is_training
        for layer in self.layers:
            layer.set_training(is_training)

    def init(self, x_observed: Array2[uint32, Batch, Features]) -> None:
        """Initialise states of the network using an ancestral sample step."""
        self.forward(m_samples=x_observed.shape[0])

    def upward(self, X: Array2[uint32, Batch, Features]):
        """Execute upward methods in sequence."""
        result = (X,)
        for layer in self.layers[::-1]:
            result = layer.upward(*result)

        return result

    def downward(self, input):
        """Execute downward methods in sequence."""
        result = input
        for layer in self.layers:
            result = layer.downward(*result)

        return result

    def forward(self, m_samples: int):
        """Acenstral sampling of sequential model."""
        result = m_samples
        for layer in self.layers:
            result = layer.forward(result)

        return result

    def joint_log_prob(self, X: Array2[uint32, Batch, Features]):
        """Joint log-likelihood of entire sequential model."""
        total_log_prob = jnp.array(0.0)
        params = X.shape[0]
        for layer in self.layers[:-1]:
            log_prob, params = layer.joint_log_prob(params)
            total_log_prob += log_prob

        # Pass the trainings data in the last layer.
        total_log_prob += self.layers[-1].joint_log_prob(params, X)
        return total_log_prob

    def log_prob(self, X: Array2[uint32, Batch, Features]):
        """Log-likelihood of of the observed data `X`."""
        return self.layers[-1].log_prob(X)

    def __call__(self, X: Array2[uint32, Batch, Features]):
        """Run upward and downward operations in sequence."""
        if hk.running_init():
            # Initialise Markov chain.
            self.init(X)
        result = self.upward(X)
        return self.downward(result)
