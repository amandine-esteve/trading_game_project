import streamlit as st
from datetime import datetime

from trading_game.config.settings import GAME_DURATION, MAX_OPTION_POSITION, STARTING_CASH
from trading_game.core.manual_trading import OrderExecutor
from trading_game.core.book import Book
from trading_game.models.stock import Stock
from trading_game.models.street import Street

from trading_game.app.utils.functions import calculate_total_portfolio_value

def initial_settings() -> None:
    st.session_state.stock = Stock.stock()
    st.session_state.street = Street.street()
    st.session_state.book = Book()
    st.session_state.order_executor = OrderExecutor(max_position_size=MAX_OPTION_POSITION)
    st.session_state.cash = STARTING_CASH
    st.session_state.starting_cash = STARTING_CASH
    st.session_state.positions = []
    st.session_state.futures_position = 0
    st.session_state.trade_history = []
    st.session_state.pnl_history = [0]
    st.session_state.tick_count = 0
    st.session_state.game_over = False

def initialize_session_state() -> None:
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.game_duration = GAME_DURATION
        st.session_state.trading_paused = False
        initial_settings()

def update_state_on_autorefresh() -> None:
    if not st.session_state.trading_paused and not st.session_state.game_over:
        if st.session_state.tick_count >= st.session_state.game_duration:
            st.session_state.game_over = True
        else:
            stock = st.session_state.stock
            tick_count = st.session_state.tick_count
            pnl_history = st.session_state.pnl_history
            positions = st.session_state.positions

            stock.move_price()
            tick_count += 1

            total_pnl = calculate_total_portfolio_value() - st.session_state.starting_cash
            pnl_history.append(total_pnl)

            for pos in positions:
                time_remaining = (pos['expiry_date'] - datetime.now()).total_seconds() / (365 * 24 * 3600)
                pos['time_to_expiry'] = max(0, time_remaining)

            st.session_state.stock = stock
            st.session_state.tick_count = tick_count
            st.session_state.pnl_history = pnl_history
            st.session_state.positions = positions
