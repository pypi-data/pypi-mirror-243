from typing import Callable

from jax import jit, random
from haiku import TransformedWithState


def scannable(
    transform_fn: TransformedWithState | Callable,
) -> Callable[[tuple, None], tuple]:
    """Transform signature of Haiku stateful-function compatible with jax scan."""
    if isinstance(transform_fn, TransformedWithState):
        transform_fn = transform_fn.apply
    _transform_fn = jit(transform_fn)  # type: ignore

    def wrapped(carry, _):
        params, state, key, *args = carry
        sub_key, key = random.split(key)
        f_out, next_state = _transform_fn(params, state, sub_key, *args)
        return (params, next_state, key, *args), f_out

    return wrapped
