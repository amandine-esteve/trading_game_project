import numpy as np
import streamlit as st

from trading_game.config.settings import TRANSACTION_COST



def render_trading_delta(portfolio_greeks) -> None:
    st.markdown('<a id="hedging"></a>', unsafe_allow_html=True)
    st.header(f"🛡️ Trading Shares - {st.session_state.stock.ticker}")

    hedge_col1, hedge_col2, hedge_col3 = st.columns([2, 2, 1])

    with hedge_col1:
        st.markdown(f"**Current Portfolio Delta:** {portfolio_greeks['delta']:.0f}")
        recommended_hedge = -portfolio_greeks['delta']
        st.markdown(f"**Recommended Hedge:** {recommended_hedge:+.0f} shares")

    with hedge_col2:
        stock_qty = st.number_input(
            "Stock Quantity",
            min_value=-10000,
            max_value=10000,
            value=int(recommended_hedge),
            step=100,
            help="Positive = Long, Negative = Short"
        )

        transaction_cost = abs(stock_qty) * st.session_state.stock.last_price * TRANSACTION_COST
        st.caption(f"Transaction cost: ${transaction_cost:.2f}")

    with hedge_col3:
        st.write("")
        st.write("")
        if st.button("⚡ Execute Hedge", type="primary"): #missing full plug
            if st.session_state.cash >= transaction_cost:
                if st.session_state.futures_position == 0 or np.sign(stock_qty) == np.sign(
                        st.session_state.futures_position):
                    total_position = st.session_state.futures_position + stock_qty
                    if st.session_state.futures_position == 0:
                        st.session_state.futures_entry_price = st.session_state.stock.last_price
                    else:
                        old_notional = st.session_state.futures_position * st.session_state.futures_entry_price
                        new_notional = stock_qty * st.session_state.stock.last_price
                        st.session_state.futures_entry_price = (old_notional + new_notional) / total_position
                    st.session_state.futures_position = total_position
                else:
                    st.session_state.futures_position += stock_qty
                    if st.session_state.futures_position == 0:
                        st.session_state.pop('futures_entry_price', None)

                st.session_state.cash -= transaction_cost
                st.success(f"Hedge executed! New position: {st.session_state.futures_position:+.0f}")

                # ADD TRADE TO BOOK
                st.session_state.book.add_trade_stock(
                    st.session_state.stock,
                    stock_qty,
                    st.session_state.stock.last_price,
                    st.session_state.stock.last_vol)

                st.rerun()
            else:
                st.error("Insufficient cash for transaction cost!")

    st.divider()