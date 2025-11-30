import streamlit as st

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
        <a href="#manual-trading" class="nav-link">💼 Manual Trading</a>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.caption(f"⏱️ Refresh: {REFRESH_INTERVAL/1_000}s")
        st.caption(f"🎮 Status: {'PAUSED' if st.session_state.trading_paused else 'ACTIVE'}")
        st.caption(f"🏁 Game: {'OVER' if st.session_state.game_over else 'IN PROGRESS'}")

def render_header(portfolio_pnl: float, score: float) -> None:
    st.title("🎯 Options Market Maker Dashboard")

    if st.session_state.game_over:
        final_pnl = portfolio_pnl
        final_score = score

        if final_pnl > 0:
            st.success(f"🎉 GAME OVER - YOU WIN! Final P&L: ${final_pnl:,.0f} | Score: {final_score:.0f}/100")
        else:
            st.error(
                f"💀 GAME OVER - Better luck next time! Final P&L: ${final_pnl:,.0f} | Score: {final_score:.0f}/100")
        st.divider()

    progress_pct = st.session_state.tick_count / st.session_state.game_duration
    time_remaining = int(
        ((st.session_state.game_duration - st.session_state.tick_count) * REFRESH_INTERVAL / 1000) // 60
    )

    col_progress1, col_progress2 = st.columns([4, 1])
    with col_progress1:
        st.progress(progress_pct,
                    text=f"Game Progress: {st.session_state.tick_count}/{st.session_state.game_duration} ticks")
    with col_progress2:
        st.metric("Time Left", f"{time_remaining} min" if time_remaining > 0 else "Last Minute")

    st.divider()