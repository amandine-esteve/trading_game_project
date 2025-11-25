import streamlit as st

def get_risk_color(value, thresholds) -> str:
    abs_val = abs(value)
    if abs_val < thresholds[0]:
        return "#00ff88"
    elif abs_val < thresholds[1]:
        return "#ffaa00"
    else:
        return "#ff4444"

def remove_st_default() -> None:
    # Remove Streamlit default top padding and toolbar
    st.markdown("""
        <style>
            header {visibility: hidden;}
            .block-container {
                padding-top: 0rem !important;
            }
            body {
                background-color: #0e1117;
            }
        </style>
    """, unsafe_allow_html=True)

def global_theme() -> None:
    # Custom CSS for dark theme
    st.markdown("""
    <style>
    /* ---------- App Background & Global Text ---------- */
    .stApp {
        background-color: #0e1117;
        color: #ffffff !important;
    }

    /* ---------- Sidebar Header Background ---------- */
    [data-testid="stSidebarHeader"] {
        background-color: #0e1117 !important;
    }

    /* ---------- Sidebar Background ---------- */

    [data-testid="stSidebar"] {
        background-color: #0e1117 !important;
    }

    /* ---------- Sidebar Navigation Title ---------- */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* ---------- Sidebar / Navigation Links ---------- */
    .nav-link {
        display: block;
        padding: 10px;
        margin: 5px 0;
        background-color: #1e2130;
        border-radius: 5px;
        text-decoration: none;
        color: white;
        text-align: center;
        transition: background-color 0.3s;
    }
    .nav-link:hover {
        background-color: #2e3444;
    }

    /* ---------- Metric Cards ---------- */
    .metric-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2e3444;
    }

    div[data-testid="stMetricLabel"] {
        color: white !important;
    }
    div[data-testid="stMetricValue"] {
        color: white !important;
        font-weight: bold;
        font-size: 28px;
    }
    div[data-testid="stMetricDelta"] {
        color: white !important;
    }

    [data-testid="stMetricLabel"], 
    [data-testid="stMetricValue"], 
    [data-testid="stMetricDelta"] {
        color: #ffffff !important;
        text-shadow: none !important;
    }

    /* ---------- Risk Coloring ---------- */
    .risk-high { color: #ff4444 !important; font-weight: bold; }
    .risk-medium { color: #ffaa00 !important; }
    .risk-low { color: #00ff88 !important; }

    /* ---------- Buttons ---------- */
    .stButton>button {
        background-color: #ff4444 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #ff6666 !important;
    }

    .stButton.secondary>button {
        background-color: #1e2130 !important;
        color: white !important;
    }

    /* ---------- Sliders, selects, inputs ---------- */
    .stSlider, .stSelectbox, .stNumberInput, .stRadio {
        color: #ffffff !important;
    }

    /* ---------- Checkbox ---------- */
    [data-baseweb="checkbox"] input:checked + div {
        background-color: #ff4444 !important;
    }
    [data-baseweb="checkbox"] label {
        color: white !important;
    }

    /* ---------- Progress Bars ---------- */
    .stProgress>div>div>div>div {
        background-color: #ff4444 !important;
    }
    .stProgress>div>div>div {
        background-color: #1e2130 !important;
        color: white !important;
    }

    /* ---------- Expanders ---------- */
    .stExpander {
        background-color: #1e2130 !important;
        color: white !important;
    }
    .stExpander .stMarkdown,
    .stExpander .stDataFrame,
    .stExpander .stText {
        color: white !important;
    }
    div[data-testid="stDataFrameContainer"] {
        color: white !important;
        background-color: #0e1117 !important;
    }
    div[data-testid="stInfo"] {
        color: white !important;
        background-color: #1e2130 !important;
        border: 1px solid #2e3444;
    }

    /* ---------- Headers / Labels / Static text ---------- */
    .css-1v3fvcr, .css-1kyxreq, .css-1q8dd3e {
        color: #ffffff !important;
    }

    /* ---------- Risk Bars (Delta, Gamma, Vega, Theta) ---------- */
    .risk-bar-container {
        position: relative;
        width: 100%;
        height: 16px;
        background-color: #2e3444;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 8px;
    }
    .risk-bar {
        height: 100%;
        position: absolute;
        top: 0;
    }

    /* ---------- Tabs: Style général ---------- */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1e2130 !important;
        gap: 5px;
        padding: 5px;
        border-radius: 8px;
    }

    /* Tabs non sélectionnées */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #2e3444 !important;
        color: #ffffff !important;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 500;
        border: none;
    }

    /* Tabs au hover */
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #3e4454 !important;
        color: #ffffff !important;
    }

    /* Tab sélectionnée */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #ff4444 !important;
        color: #ffffff !important;
        font-weight: bold;
        border-bottom: 3px solid #ff6666;
    }

    /* Texte dans les tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-size: 16px;
        margin: 0;
    }

    /* Contenu des tabs */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #1e2130 !important;
        padding: 20px;
        border-radius: 8px;
        margin-top: 10px;
    }

    /* ---------- Labels des inputs ---------- */
    label[data-testid="stWidgetLabel"] {
        color: #ffffff !important;
        font-weight: 500;
    }

    /* ---------- Radio buttons ---------- */
    /* Texte des boutons */
    /* Texte des boutons non sélectionnés */
    .stRadio > label {
        color: #ffffff !important;  /* texte blanc */
        font-weight: normal;
    }

    /* Fond neutre des boutons (non sélectionnés) */
    .stRadio [data-baseweb="radio"] > div {
        background-color: #2e3444;  /* fond sombre */
        border-radius: 8px;
        padding: 5px 0;  /* padding vertical uniquement */
        margin-right: 8px;
        display: flex;
        align-items: center;
        gap: 5px;  /* espace entre cercle et texte */
        border: 1px solid #444c5c;
        color: #ffffff !important;  /* texte blanc */
    }

    /* Bouton sélectionné : fond rouge derrière cercle + texte */
    .stRadio [data-baseweb="radio"] input:checked + div {
        background-color: #ff4444 !important;  /* rouge vif */
        color: #ffffff !important;  /* texte blanc sur fond rouge */
        border: 1px solid #ff4444 !important;
        font-weight: bold;
        padding-left: 5px;  /* ajuste cercle */
        padding-right: 5px; /* ajuste texte */
    }


    /* ---------- Selectbox ---------- */
    [data-baseweb="select"] {
        color: #ffffff !important;
    }

    [data-baseweb="select"] > div {
        background-color: #1e2130 !important;
        color: #ffffff !important;
        border-color: #2e3444 !important;
    }

    /* ---------- Input Text Color ---------- */
    [data-baseweb="input"] input {
        color: #0e1117 !important;
    }

    /* Number input text */
    [data-baseweb="base-input"] input {
        color: #0e1117 !important;
    }

    /* Text input */
    input[type="text"],
    input[type="number"] {
        color: #0e1117 !important;
    }

    /* Textarea */
    textarea {
        color: #0e1117 !important;
    }

    /* ---------- Slider ---------- */
    [data-baseweb="slider"] {
        color: #ffffff !important;
    }

    [data-baseweb="slider"] [role="slider"] {
        background-color: #ff4444 !important;
    }

    /* ---------- Expander header + visible ---------- */
    .streamlit-expanderHeader {
        background-color: #1e2130 !important;
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: 1px solid #2e3444;
        border-radius: 5px;
    }

    .streamlit-expanderHeader:hover {
        background-color: #2e3444 !important;
    }

    /* ---------- Success/Error messages ---------- */
    .stSuccess {
        background-color: #0e7a0e !important;
        color: #ffffff !important;
        border: 1px solid #00ff88 !important;
    }

    .stError {
        background-color: #a51c30 !important;
        color: #ffffff !important;
        border: 1px solid #ff4444 !important;
    }

    .stInfo {
        background-color: #1e3a5f !important;
        color: #ffffff !important;
        border: 1px solid #4a90e2 !important;
    }

    /* ---------- Markdown headings dans manual trading ---------- */
    .stMarkdown h4, .stMarkdown h3, .stMarkdown h2 {
        color: #ffffff !important;
        font-weight: bold;
    }

    .stMarkdown p {
        color: #ffffff !important;
    }

    /* ---------- Divider + visible ---------- */
    hr {
        border-color: #2e3444 !important;
        margin: 20px 0;
    }

    /* ---------- Table Styling ---------- */
    table {
        background-color: #0e1117 !important;
        color: #ffffff !important;
        width: 100%;
    }

    table th {
        background-color: #1e2130 !important;
        color: #ffffff !important;
        padding: 10px;
        font-weight: bold;
        border: 1px solid #2e3444;
    }

    table td {
        background-color: #0e1117 !important;
        color: #ffffff !important;
        padding: 8px;
        border: 1px solid #2e3444;
    }

    table tr:hover td {
        background-color: #1e2130 !important;
    }

    /* Hide index column */
    table td:first-child,
    table th:first-child {
        display: none !important;
    }

    </style>
    """, unsafe_allow_html=True)