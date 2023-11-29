from functools import partial
import os
from typing import Optional, Sequence

import chex
import einops  # type: ignore
import jax
from jax import jit, random, vmap  # type: ignore
from jaxtyping import Array, Float, UInt, PRNGKeyArray
from jax.lax import fori_loop, scan  # type: ignore
import jax.numpy as jnp
from tensorflow_probability.substrates import jax as tfp  # type: ignore
from tensor_annotations.axes import Batch, Channels, Features
from tensor_annotations.jax import Array0, Array1, Array2, Array3, float32, uint32

tfd = tfp.distributions

_BATCH_SIZE = int(os.environ.get("GABENET_BATCH_SIZE", 64))
_UNROLL_BATCHES = int(os.environ.get("GABENET_UNROLL_BATCHES", 1))


class PRNGSequence:
    def __init__(self, key):
        self._key = key

    def __next__(self):
        self._key, key = random.split(self._key)
        return key


@partial(jit, static_argnames=["shape", "dtype"])
def gamma(key, a, b, shape=None, dtype=float):
    """Sample gamma distribution.

    Args:
        a: Shape of gamma distribution.
        b: Rate (inverse scale) of gamma distribution.
    """
    x_sample = random.gamma(key, a, shape, dtype) / b
    # When x_sample falls below error tolerance, because a < 1 and b > 1, reinstate the
    # error tolerance.
    float_min = jnp.finfo(x_sample.dtype).tiny
    return jnp.maximum(x_sample, float_min)


@partial(jit, static_argnums=(2,))
def _sum_bernoullis(i: int, val: tuple, shape):
    cumulative, key, r = val
    log_p = jnp.log(r) - jnp.log(r + i)
    key, sub_key = random.split(key)
    new_cumulative = cumulative + random.bernoulli(
        sub_key, p=jnp.exp(log_p), shape=shape
    )
    return (new_cumulative, key, r)


@partial(jit, static_argnums=(3,))
@partial(vmap, in_axes=(0, 0, 0, None), out_axes=-1)
def _chinese_restaurant_table(key, n, r, shape):
    """Vectorised CRT where key, n, and r are all vectors (1-D arrays)."""
    zero = jnp.array(0, dtype=n.dtype)  # Make sure 0 and n have the same dtype.
    total_sum, _, _ = fori_loop(
        lower=zero,
        upper=n,
        body_fun=lambda i, v: _sum_bernoullis(i, v, shape),
        init_val=(jnp.zeros(shape=shape, dtype=n.dtype), key, r),
    )
    return total_sum


def chinese_restaurant_table(key, n, r, shape: Optional[Sequence[int]] = None):
    """Generate a sample from the Chinese restaurant table distribution.

    Args:
        key: Pseudo random number generator key.
        n: The number of customers in the restaurant.
        r: The concentration parameter.
        shape: Shape of output tensor (must be broadcastable with `n` and `r`).

    Returns:
        The number of tables seated by `n` customers with concentration `r`.
    """
    if shape is None:
        if jnp.shape(n) != jnp.shape(r):
            n, r = jnp.broadcast_arrays(n, r)
        shape = jnp.shape(n)
    _shape = jnp.broadcast_shapes(n.shape, shape)  # type: ignore

    n_keys = n.size
    keys = random.split(key, num=n_keys)
    n_rank = len(n.shape)

    assert len(keys) == len(n.flatten())
    l_samples = _chinese_restaurant_table(
        keys, n.flatten(), r.flatten(), _shape[: len(_shape) - n_rank]
    )
    return l_samples.reshape(_shape)


def dirichlet_multinomial(
    key, n_trials, alpha, shape: Optional[Sequence[int]] = None, dtype=jnp.uint32
):
    """Generate a sample from the Dirichlet-Multinomial distribution.

    Args:
        key: Pseudo random number generator key.
        n_trials: Number of draws from multinomial distribution.
        alpha: Dirichlet prior of shape `(..., n)`, similar to `jax.random.dirichlet`.
        shape: Shape of random variates, excluding the last shape dimension `n` of
            `alpha`.
        dtype: Cast return value to this dtype.

    Returns:
        A draw from the distribution with shape `shape + (alpha.shape[-1),)`.
    """
    if shape is None:
        n_shape = jnp.broadcast_shapes(n_trials.shape, alpha.shape[:-1])
    else:
        n_shape = jnp.broadcast_shapes(n_trials.shape, alpha.shape[:-1], shape)
    a_shape = n_shape + (alpha.shape[-1],)

    n_trials = jnp.broadcast_to(n_trials, n_shape)
    alpha = jnp.broadcast_to(alpha, a_shape)

    key, sub_key = random.split(key)
    p_dirichlet = random.dirichlet(sub_key, alpha, n_shape)
    n_trials = n_trials.astype(float)
    x_counts = tfd.Multinomial(total_count=n_trials, probs=p_dirichlet).sample(seed=key)
    return x_counts.astype(dtype)


@chex.dataclass
class _BernoulliBetaState:
    """State (`alpha_0`) and parameters of MCMC chain to sample posterior Gamma-CRT."""

    # Concentration (to MCMC sample) of the Chinese restaurant table distribution.
    alpha_0: Array0[float32]
    # Total number of occupied tables over all the Chinese restaurants (sum over restaurant occupancies).
    m_tables_total: Array0[uint32]
    # Number of customers in the Chinese restaurant.
    n_customers: Array1[uint32, Batch]
    # Shape parameter (alpha) of the Gamma prior.
    a_gamma: Array0[float32]
    # Rate parameter (beta) of the Gamma prior.
    b_gamma: Array0[float32]


def _gibbs_step_posterior_gamma_crt(carry: _BernoulliBetaState, key):
    """Do one Gibbs sample step by augmenting with Bernoulli and beta distributions.

    Reference:
        [1]: Teh, Jordan, Beal & Blei (2006) Hierarchical Dirichlet Processes,
            J Am Stat Assoc, 101:476, 1566-1581, DOI: 10.1198/016214506000000302.
    """
    n_samples = carry.n_customers.shape[0]

    # Sample according to Eq. (A.5), Ref. [1].
    key, sub_key = random.split(key)
    w = random.beta(
        sub_key, carry.alpha_0 + 1.0, carry.n_customers, shape=(n_samples,)  # type: ignore
    )

    # Sample according to Eq. (A.6), Ref. [1].
    key, sub_key = random.split(key)
    p_berno = 1 / (
        1.0 + carry.alpha_0 / carry.n_customers  # type: ignore
    )  # <==> p proportional to n / alpha_0.
    s = random.bernoulli(sub_key, p_berno, shape=(n_samples,))

    # Sample according to Eq. (A.4), Ref. [1].
    alpha = carry.a_gamma + carry.m_tables_total - jnp.sum(s)
    beta = carry.b_gamma - jnp.sum(jnp.log(w))
    key, sub_key = random.split(key)
    alpha_0 = gamma(sub_key, alpha, beta)

    carry.alpha_0 = alpha_0
    return (carry, alpha_0)


def posterior_gamma_chinese_restaurant_table(
    key,
    m: Array1[uint32, Batch],
    n: Array1[uint32, Batch],
    a: Array0[float32],
    b: Array0[float32] | float,
) -> Array0[float32]:
    r"""Sample concentration posterior of joint gamma-Chinese restaurant distribution.

    Take posterior samples from
    $$
    p(\alpha|\textbf{m},\textbf{n}, a, b) \propto
        \mathrm{Gamma}(\alpha|a, b) \prod_{i=1}^{N} \frac{\alpha^{m_i}\Gamma(\alpha)}{\Gamma(\alpha+n_i)}
    $$

    corresponding to the joint distribution Gamma-CRT distribution:
    $$
    p(\alpha, \textbf{m}|\textbf{n}, a, b) =
    \mathrm{Gamma}(\alpha|a, b) \prod_{i=1}^N \mathrm{CRT}(m_i|n_i, \alpha)
    $$
    using the Bernoulli-beta augmentation trick from Teh, Jordan, Beal & Blei Hierarchical Dirichlet Processes,
            J Am Stat Assoc, 101:476, 1566 (2006).

    Args:
        key: Pseudo random number generator key.
        m: Number of occupied tables in the Chinese restaurant (of size \(N\)).
        n: Number of customers in the Chinese restaurant (of size \(N\)).
        a: shape parameter of the Gamma prior.
        b: rate parameter of the Gamma prior.

    Returns:
        Scalar sample of the concentration parameter \(\alpha\).
    """
    n_iterations: int = 20  # See Appendix Teh.

    # Initialise Markov chain/
    key, sub_key = random.split(key)
    alpha_0 = gamma(sub_key, a, b, shape=())
    carry_init = _BernoulliBetaState(
        alpha_0=alpha_0, m_tables_total=jnp.sum(m), n_customers=n, a_gamma=a, b_gamma=b  # type: ignore
    )
    keys = random.split(key, num=n_iterations)

    # Run chain for `n_iterations` and collect a sample.
    _, alpha_0_chain = scan(_gibbs_step_posterior_gamma_crt, init=carry_init, xs=keys)
    alpha_0 = alpha_0_chain[-1]
    return alpha_0


@partial(jit, donate_argnums=(1,))
def _augmented_poisson(key, rate, x):
    # Normalise over the augmented space.
    rate_norm = jnp.sum(rate, axis=-1, keepdims=True)
    zeta = jnp.where(rate_norm == 0, 0, rate / rate_norm)
    x_augmented = tfd.Multinomial(total_count=x, probs=zeta).sample(seed=key)
    return x_augmented


def augmented_poisson(
    key,
    rate: Array3[float32, Batch, Features, Channels]
    | Array2[float32, Features, Channels],
    x: Array2[uint32, Batch, Features] | Array1[uint32, Features],
    dtype=int,
):
    r"""Sample of augmented Poisson distribution.

    That is, given:
    $$
    x_{ij} \sim \mathrm{Pois}(\sum_k \lambda_{ijk}),
    $$

    Sample:
    $$
    x_{ijk} \mid x_{ij} \sim \mathrm{Pois}(\lambda_{ijk}), \sum_k x_{ijk} = x_{ij}.
    $$

    Args:
        key: Pseudo random number generator key.
        rate: The poisson rate parameter \(\lambda_{ijk}\) by which `x` was generated after
            marginalising over the latent states (`Channels`).
        x: Counts to augment.
        dtype: Cast return value to this dtype.

    Returns:
        Augmented counts that collapse to `x` when marginalised over the latent states.
    """
    return _augmented_poisson(key, rate, x.astype(float)).astype(dtype)  # type: ignore


def _recursive_augment_reduce(
    carry,
    x_and_theta_batch: tuple[
        UInt[Array, "batch features"], Float[Array, "batch channels"]
    ],
    phi: Float[Array, "channels features"],
):
    """For one sample `i`, sample x_ijk and infer m_ik = x_i.k and x_.jk recursively."""
    (key, x_jk) = carry
    key_seq = PRNGSequence(key)
    (x_batch, theta_batch) = x_and_theta_batch
    # rate(i,j,k): θ(i,k) φ(k,j).
    rate: Float[Array, "batch features channels"] = (
        theta_batch[:, jnp.newaxis, :] * phi.T[jnp.newaxis, ...]
    )
    # x(i,j,k) ~ Mult[x(i,j), rate(i,j,k)].
    x_ijk = augmented_poisson(next(key_seq), rate, x_batch)  # type: ignore

    # Recursively sum over leading dimension so that x_jk = sum_i x_ijk.
    x_jk += jnp.sum(x_ijk, axis=0)
    m_ik = jnp.sum(x_ijk, axis=1)
    carry_out = (next(key_seq), x_jk)
    return carry_out, m_ik


def augment_reduce(
    key: PRNGKeyArray,
    a: Float[Array, "batch channels"],
    b: Float[Array, "channels features"],
    x: UInt[Array, "batch features"],
    mini_batch_size: int = _BATCH_SIZE,
) -> tuple[UInt[Array, "batch channels"], UInt[Array, "features channels"]]:
    r"""Sample augmented Poisson and reduce across indices.

    That is, sample
    $$
    x_{ijk} \mid x_{ij} \sim \mathrm{Mult}(x_{ij}, a_{ik} b_{kj}),\\
    m_{ik} = \sum_{j} x_{ijk};\quad x_{jk} = \sum_{i} x_{ijk}.
    $$

    Args:
        x: Integer valued counts to augment.
        a: Per sample $i$ (rows), the latent activation \( a_{ik} \) across topics $k$
            (columns).
        b: Per topic $k$, the distribution \( b_{kj} \) over features $j$ (columns).

    Returns:
        The pair \( (m_{ik}, x_{jk}) \) obtained after reducing over the augmented
        counts \( x_{ijk} \).
    """
    # Here, we trade of memory and speed.
    #
    # For full batch sampling (= fast), we would need to store the three index tensor
    # `a x b`, which is of size `n_components` x dataset -> too large.
    # Instead, we sample batches and recursively combine and aggregate the reduced
    # summary statistics `m_ik` and `x_jk`.
    x_jk = jnp.zeros_like(b.transpose(), dtype=x.dtype)
    carry_in = (key, x_jk)

    m_samples = len(x)

    # Trivial case when no data is observed -> is used to test prior in unit tests.
    if m_samples == 0:
        return jnp.empty(a.shape, dtype=x.dtype), x_jk

    batch_size_ = min([mini_batch_size, m_samples])
    # Slice dataset in exactly `d` batches.
    shard = lambda x: einops.rearrange(x, "(d b) ... -> d b ...", b=batch_size_)

    if m_samples > mini_batch_size:
        # To slice the dataset in exactly `d` batches, we need to pad the dataset so
        # that the total dataset size becomes of size `d x b`.
        # pad -> shard -> unpad.
        n_pad = (mini_batch_size - len(x) % mini_batch_size) % mini_batch_size
        x_pad = jnp.zeros((n_pad, x.shape[1]), x.dtype)
        x_padded = jnp.concatenate([x, x_pad], axis=0)
        a_pad = jnp.ones((n_pad, a.shape[1]), a.dtype)
        a_padded = jnp.concatenate([a, a_pad], axis=0)
        xs = (shard(x_padded), shard(a_padded))
    else:
        xs = (shard(x), shard(a))

    # Function to augment a batch of samples sample.
    augment_i_fn = partial(_recursive_augment_reduce, phi=b)
    carry_out, m_dik = jax.lax.scan(
        augment_i_fn, init=carry_in, xs=xs, unroll=_UNROLL_BATCHES
    )

    # Restore original, unbatched, dataset shape.
    unshard = lambda x: einops.rearrange(x, "d b ... -> (d b) ...", b=batch_size_)
    m_ik = unshard(m_dik)
    # Shave off padding.
    m_ik = m_ik[: len(x)]
    x_jk = carry_out[1]
    return m_ik, x_jk
