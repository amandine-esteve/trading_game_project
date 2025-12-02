from typing import Dict, Tuple

import streamlit as st

from trading_game.config.settings import BASE
from trading_game.config.maturity_config import get_maturity_options, get_short_maturity_options, get_long_maturity_options



def render_option_type_choice(key: str) -> str:
    st.markdown(
        "<span style='color:white; font-weight:bold;'>Option Type</span>",
        unsafe_allow_html=True
    )
    pricer_opt_type = st.selectbox(
        "pricer_opt_type",
        ["Call", "Put"],
        key=f"{key}_opt_type",
        label_visibility="collapsed"
    )
    return pricer_opt_type.lower()

def render_strat_type_choice(key: str) -> str:
    st.markdown(
        "<span style='color:white; font-weight:bold;'>Strategy Type</span>",
        unsafe_allow_html=True
    )
    strat_type_label = st.selectbox(
        "strat_type",
        [
            "Call Spread", "Put Spread", "Straddle", "Strangle",
            "Call Calendar Spread", "Put Calendar Spread",
            "Bull Risk Reversal", "Bear Risk Reversal",
            "Call Butterfly", "Put Butterfly",
        ],
        key=f"{key}_strat_type",
        label_visibility="collapsed"
    )
    return strat_type_label

def render_market_param_inputs(vol_ref: float, strat: bool = False) -> float:
    key = f"pricer_vol_{'strat' if strat else 'opt'}"

    st.markdown(
        "<br><span style='color:white; font-weight:bold;'>Market Parameters</span>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<span style='color:white;'>Volatility (σ)</span>",
        unsafe_allow_html=True
    )
    pricer_vol = st.number_input(
        "pricer_vol",
        value=float(vol_ref),
        min_value=0.01,
        max_value=1.0,
        step=0.01,
        format="%.4f",
        key=key,
        label_visibility="collapsed"
    )

    return pricer_vol

def render_strike_input(spot_ref: float, key_tab: str, strat: bool = False) -> float:
    key = f"{key_tab}_strike_{'strat' if strat else 'opt'}"
    st.markdown(
        "<span style='color:white;'>Strike</span>",
        unsafe_allow_html=True
    )
    pricer_strike = st.number_input(
        "pricer_strike",
        value=float(round(spot_ref, 0)),
        step=1.0,
        key=key,
        label_visibility="collapsed"
    )
    return pricer_strike

def render_double_strike_input(spot_ref: float, key: str) -> Tuple[float, float]:
    st.markdown(
        "<br><span style='color:white; font-weight:bold;'>Strikes</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<span style='color:white;'>Strike 1</span>",
        unsafe_allow_html=True
    )
    strat_k1 = st.number_input(
        "strat_k1",
        value=float(round(0.9 * spot_ref, 0)),
        step=1.0,
        key=f"{key}_strat_k1",
        label_visibility="collapsed"
    )
    st.markdown(
        "<span style='color:white;'>Strike 2</span>",
        unsafe_allow_html=True
    )
    strat_k2 = st.number_input(
        "strat_k2",
        value=float(round(1.1 * spot_ref, 0)),
        step=1.0,
        key=f"{key}_strat_k2",
        label_visibility="collapsed"
    )
    return strat_k1, strat_k2

def render_triple_strike_input(spot_ref: float, key: str) -> Tuple[float, float, float]:
    st.markdown(
        "<br><span style='color:white; font-weight:bold;'>Strikes</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<span style='color:white;'>Strike 1 (Low)</span>",
        unsafe_allow_html=True
    )
    strat_k1_fly = st.number_input(
        "strat_k1_fly",
        value=float(round(0.85 * spot_ref, 0)),
        step=1.0,
        key=f"{key}_strat_k1_fly",
        label_visibility="collapsed"
    )

    st.markdown(
        "<span style='color:white;'>Strike 2 (Mid)</span>",
        unsafe_allow_html=True
    )
    strat_k2_fly = st.number_input(
        "strat_k2_fly",
        value=float(round(spot_ref, 0)),
        step=1.0,
        key=f"{key}_strat_k2_fly",
        label_visibility="collapsed"
    )
from typing import Dict, Tuple

import streamlit as st

from trading_game.config.settings import BASE
from trading_game.config.maturity_config import get_maturity_options, get_short_maturity_options, get_long_maturity_options



def render_option_type_choice(key: str) -> str:
    st.markdown(
        "<span style='color:white; font-weight:bold;'>Option Type</span>",
        unsafe_allow_html=True
    )
    pricer_opt_type = st.selectbox(
        "pricer_opt_type",
        ["Call", "Put"],
        key=f"{key}_opt_type",
        label_visibility="collapsed"
    )
    return pricer_opt_type.lower()

def render_strat_type_choice(key: str) -> str:
    st.markdown(
        "<span style='color:white; font-weight:bold;'>Strategy Type</span>",
        unsafe_allow_html=True
    )
    strat_type_label = st.selectbox(
        "strat_type",
        [
            "Call Spread", "Put Spread", "Straddle", "Strangle",
            "Call Calendar Spread", "Put Calendar Spread",
            "Bull Risk Reversal", "Bear Risk Reversal",
            "Call Butterfly", "Put Butterfly",
        ],
        key=f"{key}_strat_type",
        label_visibility="collapsed"
    )
    return strat_type_label

def render_market_param_inputs(vol_ref: float, strat: bool = False) -> float:
    key = f"pricer_vol_{'strat' if strat else 'opt'}"

    st.markdown(
        "<br><span style='color:white; font-weight:bold;'>Market Parameters</span>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<span style='color:white;'>Volatility (σ)</span>",
        unsafe_allow_html=True
    )
    pricer_vol = st.number_input(
        "pricer_vol",
        value=float(vol_ref),
        min_value=0.01,
        max_value=1.0,
        step=0.01,
        format="%.4f",
        key=key,
        label_visibility="collapsed"
    )

    return pricer_vol

def render_strike_input(spot_ref: float, key_tab: str, strat: bool = False) -> float:
    key = f"{key_tab}_strike_{'strat' if strat else 'opt'}"
    st.markdown(
        "<span style='color:white;'>Strike</span>",
        unsafe_allow_html=True
    )
    pricer_strike = st.number_input(
        "pricer_strike",
        value=float(round(spot_ref, 0)),
        step=1.0,
        key=key,
        label_visibility="collapsed"
    )
    return pricer_strike

def render_double_strike_input(spot_ref: float, key: str) -> Tuple[float, float]:
    st.markdown(
        "<br><span style='color:white; font-weight:bold;'>Strikes</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<span style='color:white;'>Strike 1</span>",
        unsafe_allow_html=True
    )
    strat_k1 = st.number_input(
        "strat_k1",
        value=float(round(0.9 * spot_ref, 0)),
        step=1.0,
        key=f"{key}_strat_k1",
        label_visibility="collapsed"
    )
    st.markdown(
        "<span style='color:white;'>Strike 2</span>",
        unsafe_allow_html=True
    )
    strat_k2 = st.number_input(
        "strat_k2",
        value=float(round(1.1 * spot_ref, 0)),
        step=1.0,
        key=f"{key}_strat_k2",
        label_visibility="collapsed"
    )
    return strat_k1, strat_k2

def render_triple_strike_input(spot_ref: float, key: str) -> Tuple[float, float, float]:
    st.markdown(
        "<br><span style='color:white; font-weight:bold;'>Strikes</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<span style='color:white;'>Strike 1 (Low)</span>",
        unsafe_allow_html=True
    )
    strat_k1_fly = st.number_input(
        "strat_k1_fly",
        value=float(round(0.85 * spot_ref, 0)),
        step=1.0,
        key=f"{key}_strat_k1_fly",
        label_visibility="collapsed"
    )

    st.markdown(
        "<span style='color:white;'>Strike 2 (Mid)</span>",
        unsafe_allow_html=True
    )
    strat_k2_fly = st.number_input(
        "strat_k2_fly",
        value=float(round(spot_ref, 0)),
        step=1.0,
        key=f"{key}_strat_k2_fly",
        label_visibility="collapsed"
    )

    st.markdown(
        "<span style='color:white;'>Strike 3 (High)</span>",
        unsafe_allow_html=True
    )
    strat_k3_fly = st.number_input(
        "strat_k3_fly",
        value=float(round(1.15 * spot_ref, 0)),
        step=1.0,
        key=f"{key}_strat_k3_fly",
        label_visibility="collapsed"
    )
    return strat_k1_fly, strat_k2_fly, strat_k3_fly

def render_maturity_selector(
    label: str,
    key: str,
    options_func=get_maturity_options,
    default_val: str = "1M"
) -> Tuple[str, int]:
    """
    Render a selectbox for maturity selection and return selected label and days.
    
    Args:
        label: Label for the selectbox
        key: Streamlit key
        options_func: Function to get maturity options (default: get_maturity_options)
        default_val: Default maturity label to select
        
    Returns:
        Tuple of (selected_label, business_days)
    """
    options = options_func()
    labels = [l for l, _ in options]
    days_map = {l: d for l, d in options}
    
    default_idx = labels.index(default_val) if default_val in labels else 0
    
    selected_label = st.selectbox(
        label,
        labels,
        index=default_idx,
        key=key,
        label_visibility="collapsed" if label == "maturity_select" else "visible"
    )
    
    return selected_label, days_map[selected_label]


def render_maturity_input(strat: bool = False) -> float:
    key = f"pricer_mat_{'strat' if strat else 'opt'}"
    st.markdown(
        "<span style='color:white;'>Time to maturity</span>",
        unsafe_allow_html=True
    )
    
    _, days = render_maturity_selector(
        "maturity_select",
        key,
        default_val="1M"
    )
    
    return days / BASE


def render_double_maturity_input() -> Tuple[float, float]:
    # Short leg
    st.markdown(
        "<span style='color:white;'>Short Leg – Maturity</span>",
        unsafe_allow_html=True
    )
    _, short_days = render_maturity_selector(
        "short_leg_maturity",
        "strat_pricer_dte_short",
        options_func=get_short_maturity_options,
        default_val="1M"
    )
    
    # Long leg
    st.markdown(
        "<span style='color:white;'>Long Leg – Maturity</span>",
        unsafe_allow_html=True
    )
    _, long_days = render_maturity_selector(
        "long_leg_maturity",
        "strat_pricer_dte_long",
        options_func=get_long_maturity_options,
        default_val="6M"
    )
    
    # Validate that long > short
    if long_days <= short_days:
        st.warning("⚠️ Long leg maturity must be greater than short leg maturity")
    
    return short_days / BASE, long_days / BASE


def render_results(price: float, greeks: Dict[str, float]) -> None:
    st.markdown(
        "<span style='color:white; font-weight:bold;'>Option Price</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size:32px; font-weight:bold; color:#ff4b4b;'>"
        f"${price:.4f}</div>",
        unsafe_allow_html=True
    )

    with st.expander("Show Greeks", expanded=False):
        st.markdown(
            "<span style='color:white; font-weight:bold;'>Greeks</span>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<span style='font-weight:bold;'>Delta:</span> {greeks['delta']:.4f}",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<span style='font-weight:bold;'>Gamma:</span> {greeks['gamma']:.6f}",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<span style='font-weight:bold;'>Vega:</span> {greeks['vega']:.4f}",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<span style='font-weight:bold;'>Theta:</span> {greeks['theta']:.6f}",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<span style='font-weight:bold;'>Rho:</span> {greeks['rho']:.6f}",
            unsafe_allow_html=True
        )