import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

from trading_game.core.option_pricer import Strategy, Greeks
from trading_game.config.settings import BASE


def render_current_positions() -> None:
    st.markdown('<a id="positions"></a>', unsafe_allow_html=True)
    st.header("📈 Current Positions")

    book = st.session_state.book

    if not book.is_empty():
        book_for_dataframe = list()

        for strat_key, (strategy, quantity, entry_price) in book.trades.items():
            if isinstance(strategy, Strategy):
                spot = st.session_state.stock.last_price
                vol = st.session_state.stock.last_vol

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

                book_for_dataframe.append({
                    'ID': strat_key,
                    'Type': strategy.name.upper(),
                    'Strike': ", ".join(f"${s:.2f}" for s in strikes),
                    'Qtity': quantity,
                    'Entry': f"${entry_price * quantity:.2f}",
                    'Current': f"${current_price:.2f}",
                    'P&L': f"${pnl:.0f}",
                    'Delta': f"{greeks['delta'] * quantity:.0f}",
                    'Gamma': f"{greeks['gamma'] * quantity:.2f}",
                    'Expiry': ", ".join((datetime.now() + timedelta(days=int(T * BASE))).strftime('%Y-%m-%d') for T in maturities)
                })

        st.markdown("#### Option Positions")
        st.table(pd.DataFrame(book_for_dataframe))

    else:
        st.info("No open positions")

    st.markdown("")
    st.markdown("#### Stock Position") #should be handled via the book as well

    stock_col1, stock_col2, stock_col3 = st.columns(3)
    with stock_col1:
        st.metric("Position", f"{st.session_state.futures_position:+.0f} shares")
    with stock_col2:
        if 'futures_entry_price' in st.session_state and st.session_state.futures_position != 0:
            futures_pnl = (
                                  st.session_state.stock.last_price - st.session_state.futures_entry_price) * st.session_state.futures_position
            st.metric("Futures P&L", f"${futures_pnl:,.0f}")
    with stock_col3:
        if st.session_state.futures_position != 0:
            st.metric("Entry Price", f"${st.session_state.get('futures_entry_price', 0):.2f}")

    st.divider()