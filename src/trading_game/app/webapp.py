import streamlit as st
from streamlit_autorefresh import st_autorefresh

from trading_game.config.settings import REFRESH_INTERVAL
from trading_game.app.layouts.main_layout import render_main_layout
from trading_game.app.utils.state_manager import initialize_session_state, update_state_on_autorefresh
from trading_game.app.layouts.rules import show_rules_page
from utils.styling import global_theme, remove_st_default, rules_page_styling 


# PAGE CONFIG - Dark Theme
st.set_page_config(
    page_title="Options Market Maker",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main() -> None:
    remove_st_default()
    global_theme()

    # Initialize session_state for navigation
    if 'show_rules' not in st.session_state:
        st.session_state.show_rules = True
    
    if st.session_state.show_rules:
        rules_page_styling()  # CSS spécifique to the rules
        show_rules_page()
        return  
    
    # Initialize session_state (before auto-refresh!)
    initialize_session_state()

    # Add a button to go back to the rules page
    with st.sidebar:
        st.markdown("---")
        if st.button("📖 View Rules", use_container_width=True):
            st.session_state.show_rules = True
            st.rerun()

    # Auto-refresh (AFTER initialization)
    if not st.session_state.trading_paused and not st.session_state.game_over:
        st_autorefresh(interval=REFRESH_INTERVAL, key="price_refresh")
        update_state_on_autorefresh()

    # Main layout
    render_main_layout()


if __name__ == "__main__":
    main()