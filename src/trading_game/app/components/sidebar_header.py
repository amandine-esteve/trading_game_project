import streamlit as st
from pathlib import Path

from trading_game.app.components.news_alert import render_news
#from trading_game.app.utils.functions import calculate_risk_score
from trading_game.config.settings import REFRESH_INTERVAL

def render_side_bar() -> None:
    with st.sidebar:
        st.title("🧭 Navigation")
        render_news(side_bar=True)

        st.markdown("---")

        st.sidebar.markdown("""
        <a href="#market-overview" class="nav-link">📊 Market Overview</a>
        <a href="#risk-dashboard" class="nav-link">⚠️ Risk Dashboard</a>
        <a href="#positions" class="nav-link">📈 Positions</a>
        <a href="#hedging" class="nav-link">🛡️ Delta Hedging</a>
        <a href="#clients" class="nav-link">📞 Client Requests</a>
        <a href="#pricer" class="nav-link">🧮 Option Pricer</a>
        <a href="#manual-trading" class="nav-link">💼 Manual Trading</a>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.caption(f"⏱️ Refresh: {REFRESH_INTERVAL/1_000}s")
        st.caption(f"🎮 Status: {'PAUSED' if st.session_state.trading_paused else 'ACTIVE'}")
        st.caption(f"🏁 Game: {'OVER' if st.session_state.game_over else 'IN PROGRESS'}")

def render_header(portfolio_pnl: float) -> None:
    
    col1, col2 = st.columns([0.5, 5])

    with col1:
        # Use absolute path to avoid issues with working directory
        logo_path = Path(__file__).parent.parent / "images" / "logo_vf.jpeg"
        st.image(str(logo_path), width=80)

    with col2:
        st.markdown("""
        <h1 style='margin-top: -10px;'>Flow Master Dashboard</h1>
        """, unsafe_allow_html=True)

    if st.session_state.game_over:
        final_pnl = portfolio_pnl

        if final_pnl > 0:
            st.success(f"🎉 GAME OVER - YOU WIN! Final P&L: ${final_pnl:,.0f}")
        else:
            st.error(
                f"💀 GAME OVER - Better luck next time! Final P&L: ${final_pnl:,.0f}")
        st.divider()

    progress_pct = st.session_state.tick_count / st.session_state.game_duration
    time_remaining = int(
        ((st.session_state.game_duration - st.session_state.tick_count) * REFRESH_INTERVAL / 1000) // 60
    )

    col_progress1, col_progress2, col_progress3 = st.columns([8, 1, 1])
    with col_progress1:
        st.progress(progress_pct,
                    text=f"Game Progress: {st.session_state.tick_count}/{st.session_state.game_duration} ticks")
    with col_progress2:
        st.metric("Time Left", f"{time_remaining} min" if time_remaining > 0 else "Last Minute")

    with col_progress3:
        refresh = st.button("Refresh")
        if refresh:
            st.rerun()

    st.divider()