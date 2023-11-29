import time

TO_TEST = {
    "dataset_size": 1_000,
    "batch_size": 8,
    "unroll_batches": 1,
}

import os

os.environ["GABENET_BATCH_SIZE"] = str(TO_TEST["batch_size"])
os.environ["GABENET_UNROLL_BATCHES"] = str(TO_TEST["unroll_batches"])

from benchmark_setup import *

X_train = X_train[: TO_TEST["dataset_size"]]


######################################################################


keys = random.split(next(key_seq), jax.device_count())
params, state = jax.pmap(kernel.init, in_axes=(0, None))(keys, X_train)

# Warmup.
apply_fn = jax.pmap(partial(kernel.apply, X=X_train), in_axes=(None, 0, 0))
keys = random.split(next(key_seq), jax.device_count())
_, state = apply_fn(params, state, keys)
state["multinomial_dirichlet_believe/~/multinomial_layer"]["phi"].block_until_ready()

keys = random.split(next(key_seq), jax.device_count())
t0 = time.time()
_, state = apply_fn(params, state, keys)
state["multinomial_dirichlet_believe/~/multinomial_layer"]["phi"].block_until_ready()
t1 = time.time()
print(f"Time apply pmap: {t1 - t0:.2f} s ")
