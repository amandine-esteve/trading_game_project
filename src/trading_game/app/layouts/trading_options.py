import streamlit as st

from trading_game.app.components.trading_tabs import render_trading_single_option_tab, render_trading_strategy_tab
from trading_game.core.manual_trading import VanillaOrder, StrategyOrder, OrderSide, OrderType, StrategyType
from trading_game.config.settings import RF, BASE, TRANSACTION_COST
from trading_game.core.option_pricer import Option, Strategy

def process_trade(order_strategy, execution_price, qty, side) -> None:
    trade_qty = qty if side == "Buy" else -qty
    book = st.session_state.book
    cost = execution_price * trade_qty * 100
    transaction_cost = execution_price * qty * 100 * TRANSACTION_COST
    total_cost = cost + transaction_cost
    if (trade_qty >= 0 and book.cash >= total_cost) or trade_qty <= 0:
        # Add trade to book
        book = st.session_state.book
        book.add_trade_strategy(
            order_strategy,
            trade_qty * 100,
            st.session_state.stock.last_price,
            st.session_state.stock.last_vol)
        book.cash -= total_cost

        st.success(f"✅ Order executed at ${execution_price:.4f}")
        st.info(f"💰 Total cost: ${cost:.2f}")
    else:
        st.error("Insufficient cash!")

def render_trading_options() -> None:
    st.markdown('<a name="manual-trading"></a>', unsafe_allow_html=True)
    st.header(f"💼 Trading Options - {st.session_state.stock.ticker}")

    tab1, tab2 = st.tabs(["Vanilla Options", "Strategies"])

    spot_ref = st.session_state.stock.last_price
    vol_ref = st.session_state.stock.last_vol

    # ===== TAB 1: VANILLA OPTIONS =====
    with tab1:
        (
            qty, side, order_type_choice, option_type, strike, days, limit_price
        ) = render_trading_single_option_tab(spot_ref, vol_ref)

        if st.button("Execute Vanilla Trade", key="btn_vanilla"):
            # Quotity of option here is 100
            total_quantity = qty * 100

            vanilla_order = VanillaOrder(
                side=OrderSide.BUY if side == "Buy" else OrderSide.SELL,
                order_type=OrderType.MARKET if order_type_choice == "Market" else OrderType.LIMIT,
                quantity=total_quantity,
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
                    process_trade(vanilla_order_strategy, vanilla_order.executed_price, qty, side)
                else:
                    st.error("❌ Order could not be executed (check limit price)")
            else:
                st.error(f"❌ Order rejected: {vanilla_order.rejection_reason}")

    # ===== TAB 2: STRATEGIES =====
    with (tab2):
        (
            qty_strat,
            side_strat,
            order_type_strat,
            strat_type,
            strikes,
            days_strat,
            short_days_strat,
            long_days_strat,
            limit_price_strat
        ) = render_trading_strategy_tab(spot_ref, vol_ref)

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

            total_quantity_strat = qty_strat * 100

            strategy_order = StrategyOrder(
                side=OrderSide.BUY if side_strat == "Buy" else OrderSide.SELL,
                order_type=OrderType.MARKET if order_type_strat == "Market" else OrderType.LIMIT,
                quantity=total_quantity_strat, 
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

            submitted = st.session_state.order_executor.submit_order(strategy_order)
            if submitted:
                success = st.session_state.order_executor.execute_strategy_order(strategy_order, Strategy)

                if success:
                    process_trade(strategy_order_strategy, strategy_order.net_premium, qty_strat, side_strat)
                else:
                    st.error("❌ Strategy could not be executed (check limit price)")
            else:
                st.error(f"❌ Order rejected: {strategy_order.rejection_reason}")

    st.divider()