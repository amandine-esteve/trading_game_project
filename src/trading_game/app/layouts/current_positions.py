import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

from trading_game.core.option_pricer import Strategy, Greeks
from trading_game.config.settings import BASE


def render_current_positions() -> None:
    st.markdown('<a id="positions"></a>', unsafe_allow_html=True)
    st.header("📈 Current Positions")

    book = st.session_state.book
    stock = st.session_state.stock

    spot = st.session_state.stock.last_price
    vol = st.session_state.stock.last_vol

    if not book.is_empty():
        book_for_dataframe = list()

        for strat_key, (strategy, quantity, entry_price) in book.trades.items():
            if isinstance(strategy, Strategy):
 
                #  Current price of the strategy
                strat_value = strategy.price(spot, vol)
                current_price = quantity * strat_value

                # Strategy strikes
                strikes = [opt.K for opt in strategy.options]

                # Strategy maturity
                maturities = [opt.T for opt in strategy.options]

                # Greeks agrégés de la stratégie
                greeks = Greeks(strategy=strategy).all_greeks(spot, vol)

                # P&L de la stratégie depuis le book
                pnl = book.strategy_pnl(strat_key, spot, vol)

                # Cash greeks
                delta_cash = greeks["delta"] * spot * quantity
                gamma_cash = 0.5 * greeks["gamma"] * (spot ** 2) * quantity

                book_for_dataframe.append({
                    'ID': strat_key,
                    'Type': strategy.name.upper(),
                    'Strike': ", ".join(f"${s:.2f}" for s in strikes),
                    'Qtity': quantity,
                    'Entry': f"${entry_price * quantity:.2f}",
                    'Current': f"${current_price:.2f}",
                    'P&L': f"${pnl:.0f}",
                    'Delta Cash': f"{delta_cash:.0f}",
                    'Gamma Cash': f"{gamma_cash:.2f}",
                    'Expiry': ", ".join((datetime.now() + timedelta(days=int(T * BASE))).strftime('%Y-%m-%d') for T in maturities)
                })

        st.markdown("#### Option Positions")
        st.table(pd.DataFrame(book_for_dataframe))

    else:
        st.info("No open positions")

    st.markdown("")
    st.markdown("#### Stock Position")

    stock_col1, stock_col2 = st.columns(2)
    with stock_col1:
        if not book.is_empty_stock():
            st.metric("Position", f"{book.stocks[stock.ticker][1]:+.0f} shares")
        else:
            st.metric("Position", f"{0:+.0f} shares")
    with stock_col2:
        if not book.is_empty_stock():
                st.metric("Stock P&L", f"${book.stocks_pnl(spot):,.0f}")

    st.divider()