import streamlit as st

from trading_game.app.components.option_param_inputs import (
    render_option_type_choice, render_strat_type_choice, render_market_param_inputs, render_strike_input,
    render_double_strike_input, render_triple_strike_input, render_maturity_input, render_double_maturity_input,
    render_results
)
from trading_game.config.settings import RF
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

def render_single_option_pricing_tab(spot_ref: float, vol_ref: float) -> None:
    key = "pricer"

    st.subheader("Price a Single Option")

    # ---------- INPUTS ON THE LEFT / RESULTS ON THE RIGHT ----------
    input_col, result_col = st.columns([2, 1])

    # ----- PARAMETERS -----
    with input_col:
        # ---------- OPTION TYPE ----------
        pricer_opt_type = render_option_type_choice(key)

        pricer_vol = render_market_param_inputs(vol_ref)

        st.markdown(
            "<br><span style='color:white; font-weight:bold;'>Option Parameters</span>",
            unsafe_allow_html=True
        )

        # Maturity
        pricer_maturity = render_maturity_input()

        # Strike
        pricer_strike = render_strike_input(spot_ref, key)

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
    key = "pricer"
    st.subheader("Price an Options Strategy")

    # ---------- INPUTS ON THE LEFT / RESULTS ON THE RIGHT ----------
    input_col, result_col = st.columns([2, 1])

    # ===== MARKET + Maturity + STRIKES =====
    with input_col:
        strat_type_label = render_strat_type_choice(key)
        
        pricer_vol = render_market_param_inputs(vol_ref, strat=True)

        strat_data = {"r": RF}

        st.markdown(
            "<br><span style='color:white; font-weight:bold;'>Option Parameters</span>",
            unsafe_allow_html=True
        )

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
            strat_k = render_strike_input(spot_ref, key_tab=key, strat=True)
            strat_data["k"] = strat_k

        # 2 strikes : spreads, strangle, risk reversals
        elif strat_type_label in [
            "Call Spread", "Put Spread", "Strangle",
            "Bull Risk Reversal", "Bear Risk Reversal"
        ]:
            strat_k1, strat_k2 = render_double_strike_input(spot_ref, key)
            strat_data["k1"] = strat_k1
            strat_data["k2"] = strat_k2

        # 3 strikes : butterflies
        elif strat_type_label in ["Call Butterfly", "Put Butterfly"]:
            strat_k1_fly, strat_k2_fly, strat_k3_fly = render_triple_strike_input(spot_ref, key)
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

