import streamlit as st

from trading_game.models.shock import StateShock


def render_news(side_bar: bool = False) -> None:

    shock = st.session_state.shock

    if shock.shock_state == StateShock.HAPPENING or shock.shock_state == StateShock.DECAY:
        if side_bar:
            st.markdown("---")

        # Determine alert type based on shock type
        if shock.shock_type == "positive":
            st.success(f"📈 **MARKET UPDATE:** {shock.news}")
        else:  # negative
            st.error(f"📉 **MARKET ALERT:** {shock.news}")
