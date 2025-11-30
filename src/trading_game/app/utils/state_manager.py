from typing import Dict, Literal

import streamlit as st
from datetime import datetime

from trading_game.config.settings import GAME_DURATION, MAX_OPTION_POSITION
from trading_game.core.book import Book
from trading_game.core.manual_trading import OrderExecutor
from trading_game.models.shock import MarketShock, StateShock
from trading_game.models.stock import Stock
from trading_game.models.street import Street


def initial_settings() -> None:
    # Game flow
    st.session_state.tick_count = 0
    st.session_state.game_over = False

    # General
    stock = Stock.stock()
    st.session_state.stock = stock
    st.session_state.street = Street.street()
    st.session_state.book = Book()
    st.session_state.order_executor = OrderExecutor(max_position_size=MAX_OPTION_POSITION)
    st.session_state.pnl_history = [
        0]  # should this be part of book? an attribute pnl history which gets updated in compute_book_pnl method

    # Market shock
    st.session_state.shock = MarketShock.shock(name=stock.name, sector=stock.sector)
    st.session_state.shock_happened = False
    st.session_state.shocked_vol = -999

    # Quote request
    st.session_state.quote_request = None
    st.session_state.quote_request_history = list()
    st.session_state.result = None
    st.session_state.quote_chat_history = list()
    st.session_state.pending_quote = None
    st.session_state.last_quote_tick = 0
    st.session_state.quote_cleared_tick = -999

def initialize_session_state() -> None:
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.game_duration = GAME_DURATION
        st.session_state.trading_paused = False
        initial_settings()

def manage_shock(tick_count: int, stock: Stock) -> Dict[str, str | Literal['positive','negative'] | StateShock | float]:
    shock = st.session_state.shock

    # If more than 20 ticks and shock hasn't already happened a shock happens on the market
    if shock.shock_state == StateShock.NONE and tick_count >= 12 and not st.session_state.shock_happened:
        shock.trigger_shock()
        st.session_state.shock_happened = True
        st.session_state.shocked_vol = stock.init_vol * shock.vol_spike

    # If the shock just happened, the effect starts fading
    elif shock.shock_state == StateShock.HAPPENING:
        shock.decay_shock()

    # If the shock is almost gone, back to initial state
    elif shock.shock_state == StateShock.DECAY and abs(stock.last_vol - stock.init_vol) < 0.01:
        shock.stop_shock()

    shock_dict = shock.model_dump()
    st.session_state.shock = shock
    return shock_dict

def update_state_on_autorefresh() -> None:
    tick_count = st.session_state.tick_count
    if not st.session_state.trading_paused and not st.session_state.game_over:
        if tick_count >= st.session_state.game_duration:
            st.session_state.game_over = True

        else:
            stock = st.session_state.stock
            book = st.session_state.book
            pnl_history = st.session_state.pnl_history

            # Update shock
            shock_dict = manage_shock(tick_count, stock)

            # Update stock
            stock.move_stock(shock_dict, st.session_state.shocked_vol)

            # Update PNL history
            total_pnl = book.compute_book_pnl(stock.last_price, stock.last_vol)
            pnl_history.append(total_pnl)

            # Update tick count
            tick_count += 1

            st.session_state.tick_count = tick_count
            st.session_state.stock = stock
            st.session_state.pnl_history = pnl_history

def add_quote_request(message: str, quote_id: str) -> None:
    """Add a new quote request to the chat"""
    st.session_state.quote_chat_history.append({
        'type': 'request',
        'message': message,
        'quote_id': quote_id,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    })
    st.session_state.pending_quote = quote_id

def add_player_response(quote_id: str, bid: float, ask: float) -> None:
    """Add player's bid/ask response to the chat"""
    st.session_state.quote_chat_history.append({
        'type': 'player_response',
        'quote_id': quote_id,
        'bid': bid,
        'ask': ask,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    })

def add_market_response(quote_id: str, final_answer:str) -> None:
    st.session_state.quote_chat_history.append({
        'type': 'market_response',
        'quote_id': quote_id,
        'message': final_answer,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    })

    # Process result if exists (add trade to book)
    if st.session_state.result:
        book = st.session_state.book
        book.add_trade_strategy(
            st.session_state.quote_request.strat,
            st.session_state.quote_request.quantity,
            st.session_state.stock.last_price,
            st.session_state.stock.last_vol)  # check if right spot ref
        st.session_state.book = book

    st.session_state.quote_cleared_tick = st.session_state.tick_count
    st.session_state.pending_quote = None

def clear_chat() -> None:
    """Clear the chat history"""
    st.session_state.quote_chat_history = list()