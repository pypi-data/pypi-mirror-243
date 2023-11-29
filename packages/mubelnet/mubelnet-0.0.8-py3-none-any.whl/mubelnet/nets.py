from typing import Iterable, Optional

from tensor_annotations.axes import Batch, Features
from tensor_annotations.jax import Array0, Array2, float32, uint32

from mubelnet import poisson, multinomial
from mubelnet.layers import _Module, Sequential
from mubelnet.utils import to_snake_string


class _BaseBeliefNet(_Module):
    def __init__(
        self,
        input_sizes: Iterable[int],
        output_size: int,
        name: Optional[str] = None,
        is_training: bool = True,
    ):
        r"""
        Args:
            input_sizes: Sizes of the input layers along the ancestral sampling process,
                from top to bottom (bottom layer ends at observations `X`).
            output_size: Number of features in training data `X`.
            name: Name of the network.
            is_training: Whether the network is in training mode (`True`) or inference
                mode (`False`).
        """
        if name is None:
            name = to_snake_string(self.__class__.__name__)
        super().__init__(
            name=name,
        )
        self.input_sizes = tuple(input_sizes)
        self.output_size = output_size
        self.layers = Sequential([], is_training=is_training)

    def set_training(self, is_training: bool):
        self.layers.set_training(is_training)

    def __call__(self, X: Array2[uint32, Batch, Features]):
        return self.layers(X)

    def init(self, x_observed: Array2[uint32, Batch, Features]) -> None:
        """Initialise states of the network using an ancestral sample step."""
        self.forward(m_samples=x_observed.shape[0])

    def forward(self, m_samples: int) -> Array2[uint32, Batch, Features]:
        """Generate ancestral samples from the network."""
        return self.layers.forward(m_samples)

    def joint_log_prob(
        self, x_observed: Array2[uint32, Batch, Features]
    ) -> Array0[float32]:
        """Log-likelihood of the joint distribution."""
        return self.layers.joint_log_prob(x_observed)

    def log_prob(self, x_observed: Array2[uint32, Batch, Features]) -> Array0[float32]:
        """Log-likelihood of the data."""
        return self.layers.log_prob(x_observed)


class PoissonGammaBelief(_BaseBeliefNet):
    """A Poisson-Gamma belief decoder network for modelling count data.

    .. figure:: figures/poisson_gamma_belief_net.svg
        Schematic representation of the multinomial Dirichlet belief network.


    Based on the paper:

    Zhou-Cong-Chen "Augmentable gamma belief networks." J Mach Learn Res 17.1,
        5656 ('16).

    But differs in: currently has no prior for the topmost
    variables `r` (see `gabenet.poisson.CapLayer`). Does not
    use collapsed Gibbs sampling for the bottom most variables.

    See also:

    - Bottom layer of the network: `mubelnet.poisson.PoissonLayer`.

    - Top layer of the network: `mubelnet.poisson.CapLayer`.

    - Intermediate layers: `mubelnet.poisson.GammaLayer`.
    """

    def __init__(
        self,
        input_sizes: Iterable[int],
        output_size: int,
        gamma_0: float = 1.0,
        e_0: float = 1.0,
        f_0: float = 1.0,
        eta=1.0,
        name: Optional[str] = None,
        is_training: bool = True,
    ):
        r"""
        Args:
            input_sizes: Sizes of the input layers along the ancestral sampling process,
                from top to bottom (bottom layer ends at observations `X`).
            output_size: Number of features in training data `X`.
            gamma_0: Shape hyperparameter \(\gamma_0\) for the top layer Gamma
                activation. (Note that deep models don't calibrate well for gamma_0=1
                or sparser.)
            e_0: Shape hyperparameter \(e_0\) of the rate
                \(c_i^{(t+1)} \sim \mathrm{Gam}(e_0, f_0)\) controlling the (inverse)
                scale of the (gamma distributed) hidden units \(\theta_{ij}^{(t)}\). The
                same hyperparameter is used for all layers of the network.
            f_0: Similar to `e_0`, but instead the rate hyperparameter \(f_0\).
            eta: Dirichlet hyperparameter \(\eta\) on weights.
            name: Name of the network.
            is_training: Whether the network is in training mode (`True`) or inference
                mode (`False`).
        """
        super().__init__(input_sizes, output_size, name=name, is_training=is_training)
        layers: list[_Module] = [
            poisson.CapLayer(
                input_size=self.input_sizes[0], gamma_0=gamma_0, e_0=e_0, f_0=f_0
            )
        ]
        for n_in, n_out in zip(self.input_sizes[:-1], self.input_sizes[1:]):
            layers.append(
                poisson.GammaLayer(
                    input_size=n_in, output_size=n_out, e_0=e_0, f_0=f_0, eta=eta
                )
            )
        layers.append(
            poisson.PoissonLayer(
                input_size=self.input_sizes[-1], output_size=output_size, eta=eta
            )
        )
        self.layers = Sequential(layers, is_training=is_training)


class MultinomialBelief(_BaseBeliefNet):
    """A Multinomial belief network for modelling count data.

    .. figure:: figures/multinomial_belief_net.svg
        Schematic representation of the multinomial belief network.

    Differs from the `PoissonGammaBelief` network in using a multinomial instead of
    Poisson distributions (training data `X`) and gamma distributions (hidden states).

    See also:

    - Bottom layer of the network: `mubelnet.multinomial.MultinomialLayer`.

    - Top layer of the network: `mubelnet.multinomial.CapLayer`.

    - Intermediate layers: `mubelnet.multinomial.DirichletLayer`.

    """

    def __init__(
        self,
        input_sizes: Iterable[int],
        output_size: int,
        gamma_0: float = 1.0,
        e_0: float = 1.0,
        f_0: float = 1.0,
        eta=1.0,
        name: Optional[str] = None,
        is_training: bool = True,
    ):
        r"""
        Args:
            input_sizes: Sizes of the input layers along the ancestral sampling process,
                from top to bottom (bottom layer ends at observations `X`).
            output_size: Number of features in training data `X`.
            gamma_0: Shape hyperparameter \(\gamma_0\) for the Gamma activation of the
                top Dirichlet \( \theta \). For dense solutions choose `gamma_0` larger
                than top layer (i.e., `gamma_0 > input_sizes[0]`). (Note that sparse
                models don't calibrate well due the drawing of multinomials.)
            eta: Dirichlet hyperparameter \(\eta\) on weights.
            name: Name of the network.
            is_training: Whether the network is in training mode (`True`) or inference
                mode (`False`).
        """
        super().__init__(input_sizes, output_size, name=name, is_training=is_training)
        layers: list[_Module] = [
            multinomial.CapLayer(
                input_size=self.input_sizes[0],
                gamma_0=gamma_0,
                e_0=e_0,
                f_0=f_0,
            )
        ]
        for n_in, n_out in zip(self.input_sizes[:-1], self.input_sizes[1:]):
            layers.append(
                multinomial.DirichletLayer(
                    input_size=n_in, output_size=n_out, e_0=e_0, f_0=f_0, eta=eta
                )
            )
        layers.append(
            multinomial.MultinomialLayer(
                input_size=self.input_sizes[-1], output_size=output_size, eta=eta
            )
        )
        self.layers = Sequential(layers, is_training=is_training)
