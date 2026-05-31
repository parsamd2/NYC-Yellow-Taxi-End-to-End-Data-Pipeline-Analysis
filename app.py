import streamlit as st

st.set_page_config(
    page_title="NYC TLC Fare Intelligence",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #0a0a0f;
        color: #e8e8f0;
    }

    section[data-testid="stSidebar"] {
        background: #111118;
        border-right: 1px solid #2a2a3a;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        font-family: 'Space Mono', monospace !important;
        color: #f0f0ff !important;
    }

    .metric-card {
        background: #16161f;
        border: 1px solid #2a2a3a;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }

    .metric-value {
        font-family: 'Space Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #ffd24c;
    }

    .metric-label {
        font-size: 0.8rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.3rem;
    }

    .hero-banner {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border: 1px solid #2a3a5a;
        border-radius: 16px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }

    .hero-title {
        font-family: 'Space Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #ffd24c;
        margin: 0 0 0.5rem 0;
    }

    .hero-subtitle {
        color: #a0a8c0;
        font-size: 1rem;
        margin: 0;
    }

    .tag {
        display: inline-block;
        background: #1e2a3a;
        border: 1px solid #3a4a6a;
        border-radius: 6px;
        padding: 0.2rem 0.6rem;
        font-size: 0.75rem;
        font-family: 'Space Mono', monospace;
        color: #7aa0d4;
        margin: 0.2rem;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label,
    div[data-testid="stNumberInput"] label {
        color: #a0a8c0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    div[data-testid="stButton"] button {
        background: #ffd24c !important;
        color: #0a0a0f !important;
        border: none !important;
        font-family: 'Space Mono', monospace !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        width: 100%;
    }

    div[data-testid="stButton"] button:hover {
        background: #ffe080 !important;
        transform: translateY(-1px);
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Space Mono', monospace;
        font-size: 0.8rem;
        color: #888;
    }

    .stTabs [aria-selected="true"] {
        color: #ffd24c !important;
    }

    .sidebar-nav-item {
        padding: 0.6rem 1rem;
        border-radius: 8px;
        margin: 0.2rem 0;
        cursor: pointer;
        color: #a0a8c0;
        font-size: 0.9rem;
    }

    .sidebar-nav-item:hover {
        background: #1e1e2e;
        color: #ffd24c;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("""
        <div style='padding: 1rem 0; border-bottom: 1px solid #2a2a3a; margin-bottom: 1rem;'>
            <div style='font-family: Space Mono, monospace; font-size: 1.1rem; color: #ffd24c; font-weight: 700;'>TLC Intelligence</div>
            <div style='font-size: 0.75rem; color: #666; margin-top: 0.3rem;'>NYC Yellow Taxi · 2022–2026</div>
        </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["Overview", "Fare Predictor", "Congestion", "Model Performance", "Driver Earnings"],
        key="nav",
        label_visibility="collapsed"
    )

    st.markdown("""
        <div style='margin-top: 2rem; padding-top: 0.8rem; border-top: 1px solid #2a2a3a; font-size: 0.7rem; color: #444;'>
            <div>Parsa Majidifard · Deakin University</div>
            <div style='margin-top: 0.3rem;'>151M trips · Medallion Pipeline</div>
        </div>
    """, unsafe_allow_html=True)

# Route to pages
if page == "Overview":
    from views import overview
    overview.render()
elif page == "Fare Predictor":
    from views import fare_predictor
    fare_predictor.render()
elif page == "Congestion":
    from views import congestion
    congestion.render()
elif page == "Model Performance":
    from views import model_performance
    model_performance.render()
elif page == "Driver Earnings":
    from views import driver_earnings
    driver_earnings.render()
