import streamlit as st
from streamlit_autorefresh import st_autorefresh

from trading_game.config.settings import REFRESH_INTERVAL
from trading_game.app.layouts.main_layout import render_main_layout
from trading_game.app.utils.state_manager import initialize_session_state, update_state_on_autorefresh



# PAGE CONFIG - Dark Theme
st.set_page_config(
    page_title="Options Market Maker",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main() -> None:
    # Initialize session_state (before auto-refresh!)
    initialize_session_state()

    # Auto-refresh (AFTER initialization)
    if not st.session_state.trading_paused and not st.session_state.game_over:
        st_autorefresh(interval=REFRESH_INTERVAL, key="price_refresh")
        update_state_on_autorefresh()

    # Main layout
    render_main_layout()


if __name__ == "__main__":
    main()
