import streamlit as st

from trading_game.app.utils.state_manager import add_player_response, add_market_response



def render_chat() -> None:
    # Chat container with custom styling
    chat_container = st.container()
    with chat_container:
        # Display chat history
        for msg in st.session_state.quote_chat_history:
            if msg['type'] == 'request' or msg['type'] == 'market_response':
                # Quote request from market
                st.markdown(f"""
                        <div style="background-color: #d0d4db; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 80%;">
                            <small style="color: #666;">{msg['timestamp']}</small><br>
                            {msg['message']}
                        </div>
                        """, unsafe_allow_html=True)
            elif msg['type'] == 'player_response':
                # Player's response
                st.markdown(f"""
                        <div style="background-color: #a8d5a8; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 80%; margin-left: auto;">
                            <small style="color: #666;">{msg['timestamp']}</small><br>
                            <strong>You:</strong> Bid: ${msg['bid']:.2f} / Ask: ${msg['ask']:.2f}
                        </div>
                        """, unsafe_allow_html=True)

def render_input_chat() -> None:
    # Input section for pending quote
    if st.session_state.pending_quote is not None:
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            bid_price = st.number_input("Your Bid ($)", min_value=0.0, step=0.05, format="%.2f",
                                        key=f"bid_{st.session_state.pending_quote}")

        with col2:
            ask_price = st.number_input("Your Ask ($)", min_value=0.0, step=0.05, format="%.2f",
                                        key=f"ask_{st.session_state.pending_quote}")

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacer
            if st.button("Send Quote", type="primary", use_container_width=True):
                if ask_price <= bid_price:
                    st.error("Ask must be higher than Bid!")
                else:
                    # Add player response to chat
                    add_player_response(st.session_state.pending_quote, bid_price, ask_price)
                    # Evaluate response
                    result = st.session_state.quote_request.evaluate_bid_ask(bid_price, ask_price,
                                                                             st.session_state.stock.last_price,
                                                                             st.session_state.stock.last_vol)
                    st.session_state.result = result
                    final_answer = st.session_state.quote_request.generate_response_message(result)
                    # Add market response to chat
                    add_market_response(st.session_state.pending_quote, final_answer)

                    st.rerun()
    else:
        st.info("No pending quote requests. Keep trading!")