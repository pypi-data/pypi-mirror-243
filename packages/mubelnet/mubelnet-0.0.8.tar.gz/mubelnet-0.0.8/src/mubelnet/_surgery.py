from copy import deepcopy

from jaxtyping import PyTree

from mubelnet.utils import get_layer_name, get_model_name
import jax.numpy as jnp


def determine_number_to_prune(state: PyTree, min_activity: int = 1) -> int:
    """Across all chain, maximum number of latent components to prune."""
    state_pruned = deepcopy(state)

    model_name = get_model_name(state)
    layer_T = "cap_layer"
    m_k = state_pruned[f"{model_name}/~/{layer_T}"]["m_k"]

    to_prune = m_k < min_activity
    number_to_prune = jnp.min(to_prune.sum(axis=-1), axis=0)

    return number_to_prune


def prune_network(state: PyTree, n_prune: int, min_activity: int = 1) -> PyTree:
    """Prune inactive latent components from state.

    Args:
        n_prune: Maximum number of latent components to prune.
    """
    model_name = get_model_name(state)

    layer_T = "cap_layer"
    if len(state.keys()) == 2:
        layer_Tmin1 = get_layer_name("bottom", model_name)
    else:
        layer_Tmin1 = get_layer_name("middle", model_name)

    state_pruned = deepcopy(state)

    # Determine which latent components to prune.
    m_k = state_pruned[f"{model_name}/~/{layer_T}"]["m_k"]
    is_inactive = m_k < min_activity
    cum_inactive = jnp.cumsum(is_inactive)
    to_prune = is_inactive & (cum_inactive <= n_prune)

    # Prune source network before migrating states to target network.
    phi = state_pruned[f"{model_name}/~/{layer_Tmin1}"]["phi"]
    state_pruned[f"{model_name}/~/{layer_Tmin1}"]["phi"] = phi[~to_prune]

    r = state_pruned[f"{model_name}/~/{layer_T}"]["r"]
    r_pruned = r[~to_prune]
    if model_name == "multinomial_belief":
        r_pruned /= r_pruned.sum(keepdims=True)
    state_pruned[f"{model_name}/~/{layer_T}"]["r"] = r_pruned

    m_k = state_pruned[f"{model_name}/~/{layer_T}"]["m_k"]
    m_k_pruned = m_k[~to_prune]
    state_pruned[f"{model_name}/~/{layer_T}"]["m_k"] = m_k_pruned

    theta = state_pruned[f"{model_name}/~/{layer_T}"]["theta"]
    theta_pruned = theta[:, ~to_prune]
    if model_name == "multinomial_belief":
        theta_pruned /= theta_pruned.sum(axis=-1, keepdims=True)
    state_pruned[f"{model_name}/~/{layer_T}"]["theta"] = theta_pruned

    # Also update the copy of theta.
    name = name_theta_copy(layer_Tmin1, model_name)
    source_key_tmin1 = f"{model_name}/~/{layer_Tmin1}"
    state_pruned[source_key_tmin1][name] = theta_pruned

    return state_pruned


def name_theta_copy(layer_name: str, model_name) -> str:
    """What is the name of the cached theta state?"""
    if layer_name == get_layer_name("bottom", model_name):
        return "copy[theta(1)]"
    return "copy[theta(t+1)]"


def _get_target_layer_name(source_layer_name: str, model_name) -> str:
    """Infer the layer name from the expanded network."""
    bottom = get_layer_name("bottom", model_name)
    middle = get_layer_name("middle", model_name)
    if source_layer_name == bottom:
        return bottom
    elif source_layer_name == middle:
        return middle + "_1"
    elif source_layer_name.startswith(f"{middle}_"):
        layer_number = int(source_layer_name.split("_")[-1])
        return f"{middle}_{layer_number + 1}"
    elif source_layer_name == "cap_layer":
        return middle
    raise Exception("Unknown truncation")


def _convert_cap_to_middle_layer(state_source: PyTree, state_target: PyTree) -> dict:
    """The source cap state is now the gamma/dirichlet target layer."""
    model_name = get_model_name(state_source)
    middle = get_layer_name("middle", model_name)
    source_key = f"{model_name}/~/cap_layer"
    target_key = f"{model_name}/~/{middle}"
    cache_name = name_theta_copy(middle, model_name)
    result = {
        # Replace theta from source.
        "theta": state_source[source_key]["theta"],
        # Cache theta from the new layer above.
        cache_name: state_target[f"{model_name}/~/cap_layer"]["theta"],
        # Keep target `m`.
        "m": state_target[target_key]["m"],
    }
    # c and phi may be frozen, and thus not present in state (but in params).
    if "c" in state_source[source_key]:
        # Replace c by source.
        result["c"] = state_source[source_key]["c"]
    if "phi" in state_target[target_key]:
        # Keep target phi.
        result["phi"] = state_target[target_key]["phi"]
    # If Poisson gamma belief, then also copy the q parameter.
    if "q" in state_target[target_key]:
        result["q"] = state_target[target_key]["q"]
    return result


def _copy_params_to_larger_net(params_source: PyTree, params_target: PyTree) -> PyTree:
    """Change names of the pytree keys consistent with larger network params."""
    params_result = deepcopy(params_target)
    for source_layer_key, source_layer_params in params_source.items():
        # Update the name of the key.
        model_name, source_name = source_layer_key.split("/~/")
        target_name = _get_target_layer_name(source_name, model_name)
        target_layer_key = f"{model_name}/~/{target_name}"
        # Carbon copy all the source layers except the cap layer.
        params_result[target_layer_key] = source_layer_params
    return params_result


def _copy_states_to_larger_net(state_source: PyTree, state_target: PyTree) -> PyTree:
    """Convert states to larger network."""
    model_name = get_model_name(state_source)
    middle = get_layer_name("middle", model_name)
    state_result = {
        f"{model_name}/~/cap_layer": state_target[f"{model_name}/~/cap_layer"],
        f"{model_name}/~/{middle}": _convert_cap_to_middle_layer(
            state_source, state_target
        ),
    }
    for source_layer_key, source_layer_state in state_source.items():
        if source_layer_key.endswith("cap_layer"):
            continue  # This was already pre-processed.
        source_layer_name = source_layer_key.split("/~/")[1]
        target_name = _get_target_layer_name(source_layer_name, model_name)
        target_layer_key = f"{model_name}/~/{target_name}"
        # Carbon copy all the source layers except the cap layer.
        state_result[target_layer_key] = source_layer_state
    return state_result


def copy_to_larger_net(
    params_source: PyTree,
    state_source: PyTree,
    params_target: PyTree,
    state_target: PyTree,
) -> tuple[PyTree, PyTree]:
    """Turn params and states of smaller into larger network with extra layer."""
    params = _copy_params_to_larger_net(params_source, params_target)
    states = _copy_states_to_larger_net(state_source, state_target)
    return params, states
