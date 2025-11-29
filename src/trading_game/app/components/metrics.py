import streamlit as st

def render_top_metrics(total_portfolio_value, pnl, risk_score, cash_available) -> None:
    col1, col2, col3, col4, col5 = st.columns(5)
    pnl_pct = (pnl / st.session_state.starting_cash) * 100

    with col1:
        st.metric(
            st.session_state.stock.ticker,
            f"${st.session_state.stock.last_price:.2f}",
            delta=f"{st.session_state.stock.last_price - st.session_state.stock.price_history[-2]:.2f}" if len(
                st.session_state.stock.price_history) > 1 else None
        )

    with col2:
        st.metric("P&L", f"${pnl:,.0f}", delta=f"{pnl_pct:.2f}%")

    with col3:
        st.metric(
            "Portfolio Value",
            f"${total_portfolio_value:,.0f}"
        )

    with col4:
        st.metric("Cash", f"${cash_available:,.0f}")

    with col5:
        score_color = "🟢" if risk_score > 80 else "🟡" if risk_score > 40 else "🔴"
        st.metric("Risk Score", f"{score_color} {risk_score:.0f}/100")

    st.divider()
