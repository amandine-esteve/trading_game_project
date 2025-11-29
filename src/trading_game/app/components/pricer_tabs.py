from typing import Dict, Tuple, Literal

import streamlit as st

from trading_game.config.settings import RF, BASE
from trading_game.core.option_pricer import Option, Strategy, Greeks



STRAT_MAP = {
    "Call Spread": "call_spread",
    "Put Spread": "put_spread",
    "Straddle": "straddle",
    "Strangle": "strangle",
    "Call Calendar Spread": "calendar_spread",
    "Put Calendar Spread": "calendar_spread",
    "Bull Risk Reversal": "risk_reversal_bullish",
    "Bear Risk Reversal": "risk_reversal_bearish",
    "Call Butterfly": "butterfly",
    "Put Butterfly": "butterfly"
}

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

def render_strike_input(spot_ref: float, strat: bool = False) -> float:
    key = f"pricer_strike_{'strat' if strat else 'opt'}"
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

def render_double_strike_input(spot_ref: float) -> Tuple[float, float]:
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
        key="strat_pricer_k1",
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
        key="strat_pricer_k2",
        label_visibility="collapsed"
    )
    return strat_k1, strat_k2

def render_triple_strike_input(spot_ref: float) -> Tuple[float, float, float]:
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
        key="strat_pricer_k1_fly",
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
        key="strat_pricer_k2_fly",
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
        key="strat_pricer_k3_fly",
        label_visibility="collapsed"
    )
    return strat_k1_fly, strat_k2_fly, strat_k3_fly

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

def render_single_option_pricing_tab(spot_ref: float, vol_ref: float) -> None:
    st.subheader("Price a Single Option")

    # ---------- OPTION TYPE ----------
    st.markdown(
        "<span style='color:white; font-weight:bold;'>Option Type</span>",
        unsafe_allow_html=True
    )
    pricer_opt_type = st.selectbox(
        "pricer_opt_type",
        ["Call", "Put"],
        key="pricer_opt_type",
        label_visibility="collapsed"
    )
    pricer_opt_type = pricer_opt_type.lower()

    # ---------- INPUTS ON THE LEFT / RESULTS ON THE RIGHT ----------
    input_col, result_col = st.columns([2, 1])

    # ----- PARAMETERS -----
    with input_col:
        pricer_vol = render_market_param_inputs(vol_ref)

        # Maturity
        pricer_maturity = render_maturity_input()

        # Strike
        pricer_strike = render_strike_input(spot_ref)

    # ----- RESULTS + GREEKS -----
    with result_col:
        pricer_option = Option(
            K=pricer_strike,
            T=pricer_maturity,
            r=RF,
            option_type=pricer_opt_type
        )
        option_price = pricer_option.price(spot_ref, pricer_vol)

        pricer_greeks = Greeks(option=pricer_option)
        greeks_result = pricer_greeks.all_greeks(spot_ref, pricer_vol)

        render_results(option_price, greeks_result)

def render_vanilla_strategy_pricing_tab(spot_ref: float, vol_ref: float) -> None:
    st.subheader("Price an Options Strategy")

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
        key="strat_pricer_type",
        label_visibility="collapsed"
    )

    # ---------- INPUTS ON THE LEFT / RESULTS ON THE RIGHT ----------
    input_col, result_col = st.columns([2, 1])

    # ===== MARKET + STRIKES =====
    with input_col:
        pricer_vol = render_market_param_inputs(vol_ref, strat=True)

        strat_data = {"r": RF}

        # ---- Maturity ----
        if strat_type_label in ["Call Calendar Spread", "Put Calendar Spread"]:
            t_short, t_long = render_double_maturity_input()
            strat_data["t1"] = t_short
            strat_data["t2"] = t_long
        else:
            strat_maturity = render_maturity_input(strat=True)
            strat_data["t"] = strat_maturity

        # ---- Strikes ----

        # 1 strike : Straddle + Calendar spreads
        if strat_type_label in ["Straddle", "Call Calendar Spread", "Put Calendar Spread"]:
            strat_k = render_strike_input(spot_ref, strat=True)
            strat_data["k"] = strat_k

        # 2 strikes : spreads, strangle, risk reversals
        elif strat_type_label in [
            "Call Spread", "Put Spread", "Strangle",
            "Bull Risk Reversal", "Bear Risk Reversal"
        ]:
            strat_k1, strat_k2 = render_double_strike_input(spot_ref)
            strat_data["k1"] = strat_k1
            strat_data["k2"] = strat_k2

        # 3 strikes : butterflies
        elif strat_type_label in ["Call Butterfly", "Put Butterfly"]:
            strat_k1_fly, strat_k2_fly, strat_k3_fly = render_triple_strike_input(spot_ref)
            strat_data["k1"] = strat_k1_fly
            strat_data["k2"] = strat_k2_fly
            strat_data["k3"] = strat_k3_fly

        method_name = STRAT_MAP[strat_type_label]

        if method_name in ["calendar_spread", "butterfly"]:
            strat_data["option_type"] = "call" if "Call" in method_name else "put"

    # ===== RESULTS + GREEKS =====
    with result_col:
        method = getattr(Strategy, method_name)
        strategy = method(**strat_data)
        strategy_price = strategy.price(spot_ref, pricer_vol)

        strat_greeks_calc = Greeks(strategy=strategy)
        strat_greeks = strat_greeks_calc.all_greeks(spot_ref, pricer_vol)

        render_results(strategy_price, strat_greeks)

