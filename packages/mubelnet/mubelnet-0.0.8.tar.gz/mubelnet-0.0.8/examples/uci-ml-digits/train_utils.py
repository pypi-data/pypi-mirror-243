import os
from pathlib import Path
import pickle
from typing import Literal, NamedTuple

import jax
import haiku as hk


_ARTEFACT_DIR = Path(os.environ.get("ARTEFACT_DIR", "/mnt/output/"))
_ARTEFACT_DIR.mkdir(parents=True, exist_ok=True)


class TrainState(NamedTuple):
    params: hk.Params
    state: hk.State
    key: jax.Array  # type: ignore
    step: int
    model_name: Literal["multinomial_belief", "poisson_gamma_belief"]
    hidden_layer_sizes: tuple[int]


def infer_last_checkpoint_number(checkpoint_dir: Path) -> int:
    """Look in checkpoint_dir and find largest checkpoint number."""
    # List all pickle files, sort by number and load last one.
    files = sorted(checkpoint_dir.glob("checkpoint_*.pkl"))
    if len(files) == 0:
        return -1
    return int(files[-1].stem.split("_")[-1])


def save_states(state: TrainState, samples, target_dir=_ARTEFACT_DIR):
    """Extract and dump last state to disk."""
    architecture = "-".join(map(str, state.hidden_layer_sizes))
    checkpoint_dir = target_dir / state.model_name / architecture / "checkpoints"
    checkpoint_dir.mkdir(exist_ok=True, parents=True)
    sample_dir = target_dir / state.model_name / architecture / "samples"
    sample_dir.mkdir(exist_ok=True, parents=True)

    i_checkpoint = infer_last_checkpoint_number(checkpoint_dir) + 1

    print("Dumping samples to disk.")
    with open(sample_dir / f"sample_{i_checkpoint:04d}.pkl", "wb") as fo:
        pickle.dump(samples, fo)

    print(f"Saving checkpoint i={i_checkpoint}.")
    # Add leading zeros to checkpoint number.
    name = f"checkpoint_{i_checkpoint:04d}.pkl"
    with open(checkpoint_dir / name, "wb") as fo:
        pickle.dump(state, fo)

    i_checkpoint += 1


def load_last_checkpoint(
    model_name, hidden_layer_sizes, source_dir=_ARTEFACT_DIR
) -> TrainState | None:
    """Load last state from disk."""
    architecture = "-".join(map(str, hidden_layer_sizes))
    checkpoint_dir = source_dir / model_name / architecture / "checkpoints"
    files = sorted(checkpoint_dir.glob("checkpoint_*.pkl"))
    if len(files) == 0:
        print("No checkpoints found.")
        return None
    with open(files[-1], "rb") as fi:
        state = pickle.load(fi)
    i_checkpoint = int(files[-1].stem.split("_")[-1])
    print(f"Loaded checkpoint i={i_checkpoint}.")
    return state
