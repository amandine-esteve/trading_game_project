import streamlit as st

from trading_game.config.settings import TRANSACTION_COST



def render_trading_delta(portfolio_greeks, cash_available) -> None:

    stock = st.session_state.stock
    book = st.session_state.book

    st.markdown('<a id="hedging"></a>', unsafe_allow_html=True)
    st.header(f"🛡️ Trading Shares - {stock.ticker}")

    hedge_col1, hedge_col2, hedge_col3 = st.columns([2, 2, 1])

    with hedge_col1:
        st.markdown(f"**Current Portfolio Delta:** {portfolio_greeks['delta']:.0f}")
        recommended_hedge = -portfolio_greeks['delta']
        st.markdown(f"**Recommended Hedge:** {int(recommended_hedge):+.0f} shares")

    with hedge_col2:
        stock_qty = st.number_input(
            "Stock Quantity",
            min_value=-10000,
            max_value=10000,
            value=int(recommended_hedge),
            step=100,
            help="Positive = Long, Negative = Short"
        )

        transaction_cost = abs(stock_qty) * stock.last_price * TRANSACTION_COST
        st.caption(f"Transaction cost: ${transaction_cost:.2f}")

    with hedge_col3:
        st.write("")
        st.write("")
        executed = True
        if st.button("⚡ Execute Hedge", type="primary"):
            if cash_available >= transaction_cost:

                # ADD TRADE TO BOOK
                st.session_state.book.add_trade_stock(
                    stock,
                    stock_qty,
                    stock.last_price,
                    )

                book.cash -= (stock_qty * stock.last_price + transaction_cost)
                st.success(f"Hedge executed! New position: {book.stocks[stock.ticker][1]:+.0f}")

            else:
                executed = False
    if executed:
        st.success(f"Hedge executed! New position: {book.stocks[stock.ticker][1]:+.0f}")
    else:
        st.error("Insufficient cash for transaction cost!")

    st.divider()