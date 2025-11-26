import streamlit as st

import plotly.graph_objects as go

def render_stock_chart(x_values) -> None:
    fig = go.Figure()
    y_values = st.session_state.stock.price_history

    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        name='Underlying',
        line=dict(color='#00d4ff', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.15)'
    ))

    if not st.session_state.game_over:
        fig.add_vline(
            x=st.session_state.tick_count,
            line_dash="dash",
            line_color="#ffaa00",
            opacity=0.5
        )

    # === Dynamically set y-axis range to give visual breathing room ===
    y_min = min(y_values)
    y_max = max(y_values)
    y_range = y_max - y_min if y_max != y_min else 1
    padding = y_range * 0.3  # 30% padding top/bottom for better centering

    fig.update_layout(
        plot_bgcolor='#1e2130',
        paper_bgcolor='#1e2130',
        font=dict(color='#ffffff'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#2e3444',
            title="Time (ticks)",
            range=[0, st.session_state.game_duration],
            zeroline=True,
            zerolinecolor='#2e3444'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2e3444',
            title="Price ($)",
            range=[y_min - padding, y_max + padding],
            zeroline=False
        ),
        height=400,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

def render_pnl_chart(x_values, pnl) -> None:
    fig_pnl = go.Figure()
    fig_pnl.add_trace(go.Scatter(
        x=x_values,
        y=st.session_state.pnl_history,
        mode='lines',
        name='P&L',
        line=dict(color='#00ff88' if pnl > 0 else '#ff4444', width=2.5),
        fill='tozeroy',
        fillcolor=f'rgba(0, 255, 136, 0.15)' if pnl > 0 else 'rgba(255, 68, 68, 0.15)'
    ))

    if not st.session_state.game_over:
        fig_pnl.add_vline(
            x=st.session_state.tick_count,
            line_dash="dash",
            line_color="#ffaa00",
            opacity=0.5
        )

    fig_pnl.update_layout(
        plot_bgcolor='#1e2130',
        paper_bgcolor='#1e2130',
        font=dict(color='#ffffff'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#2e3444',
            title="Time (ticks)",
            range=[0, st.session_state.game_duration],
            zeroline=True,
            zerolinecolor='#2e3444'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2e3444',
            title="P&L ($)",
            zeroline=True,
            zerolinecolor='#ffaa00'
        ),
        height=250,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False
    )

    st.plotly_chart(fig_pnl, use_container_width=True)