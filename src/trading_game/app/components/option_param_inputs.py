from typing import Dict, Tuple

import streamlit as st

from trading_game.config.settings import BASE



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

def render_maturity_input(strat: bool = False) -> float:
    key = f"pricer_mat_{'strat' if strat else 'opt'}"
    st.markdown(
        "<span style='color:white;'>Time to maturity (days)</span>",
        unsafe_allow_html=True
    )
    strat_maturity_days = st.slider(
        "strat_mat_days",
        min_value=1,
        max_value=365,
        value=30,
        key=key,
        label_visibility="collapsed"
    )
    strat_maturity = strat_maturity_days / BASE
    return strat_maturity

def render_double_maturity_input() -> Tuple[float, float]:
    st.markdown(
        "<span style='color:white;'>Short Leg – Days to Expiry</span>",
        unsafe_allow_html=True
    )
    strat_short_days = st.slider(
        "strat_short_days",
        min_value=1,
        max_value=365,
        value=30,
        key="strat_pricer_dte_short",
        label_visibility="collapsed"
    )
    st.markdown(
        "<span style='color:white;'>Long Leg – Days to Expiry</span>",
        unsafe_allow_html=True
    )
    strat_long_days = st.slider(
        "strat_long_days",
        min_value=2,
        max_value=730,
        value=180,
        key="strat_pricer_dte_long",
        label_visibility="collapsed"
    )
    t_short = strat_short_days / 365.0
    t_long = strat_long_days / 365.0
    return t_short, t_long

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