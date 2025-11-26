import random

import streamlit as st
from mypy.literals import literal

from trading_game.app.utils.state_manager import add_quote_request, clear_chat
from trading_game.core.quote_request import QuoteRequest



def manage_quote_requests(current_tick: int) -> None:
    """
    Manages the timing of quote requests
    current_tick: the current tick count from st.session_state.tick_count
    """

    # Clear chat one tick after market response
    if current_tick == st.session_state.quote_cleared_tick + 2:
        clear_chat()

        # Reset for next quote
        st.session_state.quote_request = None
        st.session_state.result = None

    # Check if it's time for a new quote request
    # First quote at tick 3, then every 3 ticks after previous quote
    if current_tick == 3 and st.session_state.last_quote_tick == 0:
        # First quote request
        investor = random.choice(st.session_state.street.investors)
        level = literal('easy') if len(st.session_state.quote_request_history) <= 3 else literal('hard')
        quote_request = QuoteRequest(investor=investor, level=level, init_price=st.session_state.stock.last_price)
        st.session_state.quote_request = quote_request
        st.session_state.quote_request_history.append(quote_request)

        quote_id = f"q_{current_tick}"
        message = quote_request.generate_request_message()
        add_quote_request(message, quote_id)
        st.session_state.last_quote_tick = current_tick

    elif (st.session_state.quote_cleared_tick > 0 and
          current_tick == st.session_state.quote_cleared_tick + 3):
        # New quote request 3 ticks after the last one was cleared
        investor = random.choice(st.session_state.street.investors)
        level = literal('easy') if len(st.session_state.quote_request_history) <= 3 else literal('hard')
        quote_request = QuoteRequest(investor=investor, level=level, init_price=st.session_state.stock.last_price)
        st.session_state.quote_request = quote_request
        st.session_state.quote_request_history.append(quote_request)

        quote_id = f"q_{current_tick}"
        message = quote_request.generate_request_message()
        add_quote_request(message, quote_id)
        st.session_state.last_quote_tick = current_tick