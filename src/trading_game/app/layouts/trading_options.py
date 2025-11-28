from datetime import datetime, timedelta

import streamlit as st

from trading_game.core.manual_trading import VanillaOrder, StrategyOrder, OrderSide, OrderType, StrategyType
from trading_game.config.settings import RF, BASE
from trading_game.core.option_pricer import Option, Strategy


def render_trading_options() -> None:
    st.markdown('<a name="manual-trading"></a>', unsafe_allow_html=True)
    st.header(f"💼 Trading Options - {st.session_state.stock.ticker}")
    tab1, tab2 = st.tabs(["Vanilla Options", "Strategies"])

    # ===== TAB 1: VANILLA OPTIONS =====
    with tab1:
        st.markdown("#### Buy/Sell Single Options")

        col1, col2 = st.columns(2)

        with col1:
            side = st.radio("Side", ["Buy", "Sell"], horizontal=True, key="vanilla_side")
            option_type = st.selectbox("Type", ["call", "put"], key="vanilla_type")
            strike = st.number_input(
                "Strike",
                value=float(st.session_state.stock.last_price),
                step=5.0,
                key="vanilla_strike"
            )

        with col2:
            days = st.slider("Days to Expiry", 1, 365, 30, key="vanilla_dte")
            qty = st.number_input("Quantity", min_value=1, value=1, key="vanilla_qty")
            order_type_choice = st.radio(
                "Order Type", ["Market", "Limit"], horizontal=True, key="vanilla_order_type"
            )

            if order_type_choice == "Limit":
                limit_price = st.number_input(
                    "Limit Price", min_value=0.01, value=1.0, step=0.1, key="vanilla_limit"
                )
            else:
                limit_price = None

        if st.button("Execute Vanilla Trade", key="btn_vanilla"):
            vanilla_order = VanillaOrder(
                side=OrderSide.BUY if side == "Buy" else OrderSide.SELL,
                order_type=OrderType.MARKET if order_type_choice == "Market" else OrderType.LIMIT,
                quantity=qty,
                option_type=option_type,
                strike=strike,
                maturity=days / BASE,
                spot_price=st.session_state.stock.last_price,
                volatility=st.session_state.stock.last_vol,
                risk_free_rate=RF,
                limit_price=limit_price
            )

            # Turn to strategy object
            vanilla_order_strategy = vanilla_order.to_strategy()

            submitted = st.session_state.order_executor.submit_order(vanilla_order)
            if submitted:
                success = st.session_state.order_executor.execute_vanilla_order(vanilla_order, Option)

                if success:
                    cost = vanilla_order.executed_price * qty * 100
                    st.session_state.cash += -cost if side == "Buy" else cost
                    
                    # Add trade to book
                    book = st.session_state.book
                    book.add_trade_strategy(
                    vanilla_order_strategy,
                    qty * 100,
                    st.session_state.stock.last_price,
                    st.session_state.stock.last_vol)
                    st.session_state.book = book

                    st.success(f"✅ {side} order executed at ${vanilla_order.executed_price:.4f}")
                    st.info(f"💰 Total cost: ${cost:.2f}")
                    st.rerun()
                else:
                    st.error("❌ Order could not be executed (check limit price)")
            else:
                st.error(f"❌ Order rejected: {vanilla_order.rejection_reason}")

    # ===== TAB 2: STRATEGIES =====
    with tab2:
        st.markdown("#### Execute Option Strategy Trade")

        strat_type = st.selectbox(
            "Strategy Type",
            [
                "Call Spread",
                "Put Spread",
                "Straddle",
                "Strangle",
                "Call Calendar Spread",
                "Put Calendar Spread",
                "Bull Risk Reversal",
                "Bear Risk Reversal",
                "Call Butterfly",
                "Put Butterfly"
            ],
            key="strat_type"
        )

        col1, col2 = st.columns(2)

        with col1:
            side_strat = st.radio("Side", ["Buy", "Sell"], horizontal=True, key="strat_side")

            # ===== 2 STRIKES =====
            if strat_type in [
                "Call Spread",
                "Put Spread",
                "Strangle",
                "Bull Risk Reversal",
                "Bear Risk Reversal"
            ]:
                strike1 = st.number_input(
                    "Strike 1",
                    value=float(st.session_state.stock.last_price * 0.95),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k1"
                )
                strike2 = st.number_input(
                    "Strike 2",
                    value=float(st.session_state.stock.last_price * 1.05),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k2"
                )
                strikes = [strike1, strike2]

            # ===== 3 STRIKES (BUTTERFLIES) =====
            elif strat_type in ["Call Butterfly", "Put Butterfly"]:
                strike1 = st.number_input(
                    "Strike 1 (Low)",
                    value=float(st.session_state.stock.last_price * 0.90),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k1_fly"
                )
                strike2 = st.number_input(
                    "Strike 2 (Mid)",
                    value=float(st.session_state.stock.last_price),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k2_fly"
                )
                strike3 = st.number_input(
                    "Strike 3 (High)",
                    value=float(st.session_state.stock.last_price * 1.10),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k3_fly"
                )
                strikes = [strike1, strike2, strike3]

            # ===== 1 STRIKE (STRADDLE + CALENDARS) =====
            else:  # Straddle, Call Calendar Spread, Put Calendar Spread
                label = "Strike (ATM)" if strat_type == "Straddle" else "Strike"
                strike_atm = st.number_input(
                    label,
                    value=float(st.session_state.stock.last_price),
                    min_value=0.0001,
                    step=5.0,
                    key="strat_k"
                )
                strikes = [strike_atm]

        with col2:
            # ---- Maturities ----
            if strat_type in ["Call Calendar Spread", "Put Calendar Spread"]:
                short_days_strat = st.slider(
                    "Short Leg - Days to Expiry",
                    1, 365, 30,
                    key="strat_dte_short"
                )
                long_days_strat = st.slider(
                    "Long Leg - Days to Expiry",
                    2, 730, 180,
                    key="strat_dte_long"
                )
                days_strat = long_days_strat
            else:
                days_strat = st.slider(
                    "Days to Expiry",
                    1, 365, 30,
                    key="strat_dte"
                )

            qty_strat = st.number_input("Quantity", min_value=1, value=1, key="strat_qty")
            order_type_strat = st.radio(
                "Order Type", ["Market", "Limit"], horizontal=True, key="strat_order_type"
            )

            if order_type_strat == "Limit":
                limit_price_strat = st.number_input(
                    "Limit Price", min_value=0.01, value=1.0, step=0.1, key="strat_limit"
                )
            else:
                limit_price_strat = None

        if st.button("Execute Strategy", key="btn_strategy"):
            strat_type_map = {
                "Call Spread": StrategyType.CALL_SPREAD,
                "Put Spread": StrategyType.PUT_SPREAD,
                "Straddle": StrategyType.STRADDLE,
                "Strangle": StrategyType.STRANGLE,
                "Call Calendar Spread": StrategyType.CALL_CALENDAR_SPREAD,
                "Put Calendar Spread": StrategyType.PUT_CALENDAR_SPREAD,
                "Bull Risk Reversal": StrategyType.BULL_RISK_REVERSAL,
                "Bear Risk Reversal": StrategyType.BEAR_RISK_REVERSAL,
                "Call Butterfly": StrategyType.CALL_BUTTERFLY,
                "Put Butterfly": StrategyType.PUT_BUTTERFLY,
            }

            strategy_order = StrategyOrder(
                side=OrderSide.BUY if side_strat == "Buy" else OrderSide.SELL,
                order_type=OrderType.MARKET if order_type_strat == "Market" else OrderType.LIMIT,
                quantity=qty_strat,
                strategy_type=strat_type_map[strat_type],
                strikes=strikes,
                maturity=days_strat / BASE,
                short_maturity=short_days_strat / BASE if strat_type in ["Call Calendar Spread",
                                                                        "Put Calendar Spread"] else None,
                long_maturity=long_days_strat / BASE if strat_type in ["Call Calendar Spread",
                                                                      "Put Calendar Spread"] else None,
                spot_price=st.session_state.stock.last_price,
                volatility=st.session_state.stock.last_vol,
                risk_free_rate=RF,
                limit_price=limit_price_strat
            )

            # Turn to strategy object
            strategy_order_strategy = strategy_order.to_strategy()
            #if we use the same function as above the part just below is exactly the same as for single option
            #write function submit_trade?

            submitted = st.session_state.order_executor.submit_order(strategy_order)
            if submitted:
                success = st.session_state.order_executor.execute_strategy_order(strategy_order, Strategy)

                if success:
                    cost = strategy_order.net_premium * qty_strat * 100
                    st.session_state.cash += -cost if side_strat == "Buy" else cost

                    # Add trade to book
                    book = st.session_state.book
                    book.add_trade_strategy(
                    strategy_order_strategy,
                    qty_strat * 100,
                    st.session_state.stock.last_price,
                    st.session_state.stock.last_vol)
                    st.session_state.book = book

                    st.success(f"✅ {strat_type} executed at ${strategy_order.net_premium:.4f}")
                    st.info(f"💰 Total cost: ${cost:.2f}")
                    st.rerun()
                else:
                    st.error("❌ Strategy could not be executed (check limit price)")
            else:
                st.error(f"❌ Order rejected: {strategy_order.rejection_reason}")

    st.divider()