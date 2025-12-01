import streamlit as st

from trading_game.app.components.option_param_inputs import (
    render_option_type_choice, render_strat_type_choice, render_strike_input, render_double_strike_input,
    render_triple_strike_input
)



def render_trading_single_option_tab(spot_ref: float, vol_ref: float):
    key = "trading"
    st.subheader("Buy/Sell Single Options")

    col1, col2 = st.columns(2)

    with col1:
        # ---------- SIDE ----------
        st.markdown(
            "<span style='color:white; font-weight:bold;'>Side</span>",
            unsafe_allow_html=True
        )
        side = st.radio("Side", ["Buy", "Sell"], horizontal=True, key="option_side", label_visibility="collapsed")

        # ---------- OPTION TYPE ----------
        option_type = render_option_type_choice(key)

        # ---------- OPTION STRIKE ----------
        strike = render_strike_input(spot_ref, key)

    with col2:
        # Maturity
        days = st.slider("Time to maturity (days)", 1, 365, 30, key="vanilla_dte")

        qty = st.number_input(
            "Quantity (lots)",
            min_value=1,
            value=1,
            key="vanilla_qty",
            help="1 option batch = 100 options"
        )

        st.caption(f"📦 Total options: {qty * 100}")

        order_type_choice = st.radio(
            "Order Type", ["Market", "Limit"], horizontal=True, key="vanilla_order_type"
        )

        if order_type_choice == "Limit":
            limit_price = st.number_input(
                "Limit Price (per option)",
                min_value=0.01,
                value=1.0,
                step=0.1,
                key="vanilla_limit"
            )
        else:
            limit_price = None

    return qty, side, order_type_choice, option_type, strike, days, limit_price

def render_trading_strategy_tab(spot_ref: float, vol_ref: float):
    key = "trading"
    days_strat, short_days_strat, long_days_strat = 0, 0, 0

    st.subheader("Execute Option Strategy Trade")

    strat_type = render_strat_type_choice(key)

    col1, col2 = st.columns(2)

    with col1:
        # ---------- SIDE ----------
        st.markdown(
            "<span style='color:white; font-weight:bold;'>Side</span>",
            unsafe_allow_html=True
        )
        side_strat = st.radio("Side", ["Buy", "Sell"], horizontal=True, key="strat_side", label_visibility="collapsed")

        # ===== 2 STRIKES =====
        if strat_type in [
            "Call Spread",
            "Put Spread",
            "Strangle",
            "Bull Risk Reversal",
            "Bear Risk Reversal"
        ]:
            strike1, strike2 = render_double_strike_input(spot_ref, key)
            strikes = [strike1, strike2]

        # ===== 3 STRIKES (BUTTERFLIES) =====
        elif strat_type in ["Call Butterfly", "Put Butterfly"]:
            strike1, strike2, strike3 = render_triple_strike_input(spot_ref, key)
            strikes = [strike1, strike2, strike3]

        # ===== 1 STRIKE (STRADDLE + CALENDARS) =====
        else:  # Straddle, Call Calendar Spread, Put Calendar Spread
            strike_atm = render_strike_input(spot_ref, key_tab=key, strat=True)
            strikes = [strike_atm]

    with col2:
        # ---- Maturities ----
        if strat_type in ["Call Calendar Spread", "Put Calendar Spread"]:
            short_days_strat = st.slider(
                "Short Leg - Time to maturity (days)",
                1, 365, 30,
                key="strat_dte_short"
            )
            long_days_strat = st.slider(
                "Long Leg - Time to maturity (days)",
                2, 730, 180,
                key="strat_dte_long"
            )
            days_strat = long_days_strat
        else:
            days_strat = st.slider(
                "Time to maturity (days)",
                1, 365, 30,
                key="strat_dte"
            )

        qty_strat = st.number_input(
            "Quantity (lots)",
            min_value=1,
            value=1,
            key="strat_qty",
            help="1 option batch = 100 options"
        )

        st.caption(f"📦 Total options: {qty_strat * 100}")

        order_type_strat = st.radio(
            "Order Type", ["Market", "Limit"], horizontal=True, key="strat_order_type"
        )

        if order_type_strat == "Limit":
            limit_price_strat = st.number_input(
                "Limit Price (per option)",
                min_value=0.01,
                value=1.0,
                step=0.1,
                key="strat_limit"
            )
        else:
            limit_price_strat = None

    return qty_strat, side_strat, order_type_strat, strat_type, strikes, days_strat, short_days_strat, long_days_strat, limit_price_strat