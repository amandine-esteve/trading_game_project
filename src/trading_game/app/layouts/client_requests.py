import streamlit as st

from trading_game.app.components.client_chat import render_chat, render_input_chat
from trading_game.app.utils.client_request_manager import manage_quote_requests



def render_client_requests() -> None:
    st.markdown('<a id="clients"></a>', unsafe_allow_html=True)
    st.header("📞 Client Requests")

    # Manage quote requests based on current tick
    if 'tick_count' in st.session_state:
        manage_quote_requests(st.session_state.tick_count)

    # Display chat with client
    render_chat()
    render_input_chat()

    st.divider()