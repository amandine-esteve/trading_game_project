import streamlit as st

def render_risk_bar(value, max_abs) ->None :
    """
    Render a horizontal bar where negative values fill to the left in red,
    positive values fill to the right in blue.
    max_abs is the maximum absolute value for scaling.
    """
    # Clamp value to [-max_abs, max_abs]
    value = max(-max_abs, min(max_abs, value))
    # Calculate percentage
    pct = abs(value) / max_abs * 50  # 50% is half of the bar
    color = "#00aaff" if value >= 0 else "#ff4444"
    direction = "left" if value >= 0 else "right"

    html = f"""
    <div style="position: relative; width: 100%; height: 20px; background-color: #2e3444; border-radius: 10px;">
        <div style="
            position: absolute;
            {direction}: 50%;
            width: {pct}%;
            height: 100%;
            background-color: {color};
            border-radius: 8px;
        "></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)