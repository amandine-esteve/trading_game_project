import streamlit as st

from trading_game.app.utils.state_manager import initial_settings



def render_controls() -> None:
    st.header("🎮 Game Controls")

    control_col1, control_col2 = st.columns(2)

    with control_col1:
        if st.button("⏸️ Pause" if not st.session_state.trading_paused else "▶️ Resume", use_container_width=True,
                     type="primary"):
            st.session_state.trading_paused = not st.session_state.trading_paused
            st.rerun()

    with control_col2:
        if st.button("🔄 Reset Game", use_container_width=True, type="primary"):
            initial_settings()
            st.rerun()