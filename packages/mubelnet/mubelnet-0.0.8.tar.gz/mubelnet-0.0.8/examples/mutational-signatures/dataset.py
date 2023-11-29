from pathlib import Path

from mubelnet.utils import holdout_split
import haiku as hk
import jax.numpy as jnp
import pandas as pd


_PATH = Path(__file__).parent
_COSMIC_PATH = _PATH / "COSMIC_v3.3_SBS_GRCh37.txt"
COSMIC_WEIGHTS = pd.read_csv(_COSMIC_PATH, sep="\t", index_col=0).T


def _read_sbs96(filename: str) -> pd.DataFrame:
    df = pd.read_csv(_PATH / filename)
    # Get path of this file and read mutation spectrum.
    df["Type"] = (
        df.Trinucleotide.str[0]
        + "["
        + df["Mutation type"]
        + "]"
        + df.Trinucleotide.str[2]
    )
    # The purpose of this temporary index is for sorting.
    df["sortable_index"] = (
        "[" + df["Mutation type"].str[:3] + "]" + df.Trinucleotide.str[:3]
    )
    df = df.reset_index()
    # Drop sorting index from dataframe.
    df = df.set_index("Type").sort_index()
    df = df.drop(columns=["sortable_index", "index", "Mutation type", "Trinucleotide"])
    df = df.transpose()
    assert jnp.all(df.columns == COSMIC_WEIGHTS.columns)
    return df


def _build_mutation_spectrum(random_state=42):
    key_seq = hk.PRNGSequence(random_state)
    df_pcawg = _read_sbs96("WGS_PCAWG.96.csv")
    df_other = _read_sbs96("WGS_Other.96.csv")
    df = pd.concat([df_pcawg, df_other], axis="rows")

    # The following code is for de novo training, which is currently not used.

    # # Separate hold out of lung adeno carcinoma.
    # x_cancer_types = df.index.map(lambda x: x.split("::")[0]).astype("category")
    # is_lung_adeno = x_cancer_types == "Lung-AdenoCA"
    # X_lung_adeno = df[is_lung_adeno].to_numpy()
    # df_train, df_test = train_test_split(df[~is_lung_adeno])
    # X_train, X_test = df_train.to_numpy(), df_test.to_numpy()
    # X_test_A, X_test_B = holdout_split(next(key_seq), X_test, test_size=0.8)
    # X_test_ood_A, X_test_ood_B = holdout_split(
    #     next(key_seq), X_lung_adeno, test_size=0.8
    # )
    X_train, X_test = holdout_split(next(key_seq), df.to_numpy(), test_size=0.5)
    return X_train, X_test


def load_mutation_spectrum(random_state=42):
    if not (_PATH / "train.npy").exists():
        X_train, X_test = _build_mutation_spectrum(random_state=random_state)
        jnp.save(_PATH / "train.npy", X_train)
        jnp.save(_PATH / "test.npy", X_test)
    else:
        X_train = jnp.load(_PATH / "train.npy")
        X_test = jnp.load(_PATH / "test.npy")
    return X_train, X_test
