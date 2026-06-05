import streamlit as st
import yfinance as yf
import requests
import datetime
from free_terminal import render_free_terminal
from pro_terminal import render_pro_terminal

# 1. PAGE CONFIG & GLOBAL HEX STYLING
# Preserving your complete aesthetic, including the neon grid SVG and glowing effects.
st.set_page_config(page_title="ALPHA-TERMINAL", layout="wide")

st.markdown("""
    <style>
    /* GLOBAL LAYOUT & BACKGROUND */
    [data-testid="stAppViewContainer"] {
        background-color: #000000;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='100' viewBox='0 0 56 100'%3E%3Cpath d='M28 66L0 50L0 16L28 0L56 16L56 50L28 66L28 100' fill='none' stroke='%2300f2ff' stroke-width='0.5' opacity='0.25'/%3E%3C/svg%3E");
        background-attachment: fixed;
        color: #ffffff;
    }
    [data-testid="stSidebar"] { 
        background-color: #03070b; border-right: 1px solid #00f2ff;
        box-shadow: 4px 0 15px rgba(0, 242, 255, 0.15);
    }
    /* TYPOGRAPHY */
    h1, h2, h3 { color: #00f2ff !important; text-shadow: 0 0 8px #00f2ff; font-family: 'Courier New', monospace; text-transform: uppercase;}
    /* UI ELEMENTS */
    .stMetric { background: rgba(11, 20, 32, 0.8) !important; border: 1px solid #00f2ff !important; border-radius: 10px !important; padding: 15px !important; transition: all 0.3s ease;}
    .stMetric:hover { transform: translateY(-2px); box-shadow: 0 0 15px rgba(0, 242, 255, 0.5); }
    .stButton>button, [data-testid="stLinkButton"]>a { 
        background: linear-gradient(135deg, #00f2ff 0%, #0072ff 100%) !important; color: #000000 !important; 
        font-weight: bold !important; width: 100% !important; border: none !important; border-radius: 4px !important;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.4) !important; text-decoration: none !important; text-align: center !important;
        display: inline-block !important; transition: all 0.2s ease !important;
    }
    .stButton>button:hover, [data-testid="stLinkButton"]>a:hover { filter: brightness(1.2); box-shadow: 0 0 20px rgba(0, 242, 255, 0.7) !important; }
    .lock-box { background: rgba(15, 5, 5, 0.6); border: 2px dashed #ff3333; border-radius: 8px; padding: 30px; text-align: center; }
    
    /* TAB NAVIGATION STYLING */
    button[data-baseweb="tab"] { font-family: 'Courier New', monospace; font-weight: bold; }
    div[data-baseweb="tab-list"] { background-color: transparent !important; }
    div[data-baseweb="tab-list"] div[role="presentation"] { background-color: #00f2ff !important; }
    div[data-baseweb="tab-list"] button[aria-selected="true"] { color: #00f2ff !important; border-bottom: 2px solid #00f2ff !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA ENGINE
@st.cache_data(ttl=3600)
def get_stock_data_func(ticker, range_type="free"):
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    try:
        stock = yf.Ticker(ticker.upper(), session=session)
        hist = stock.history(period="1mo")
        info = stock.info
        return info, hist
    except Exception:
        return {}, None

CANDIDATE_POOL = ["NVDA", "AAPL", "TSLA", "MSFT", "GOOGL", "AVGO", "META", "AMZN", "NFLX", "AMD", "SMCI", "ARM", "ORCL", "PLTR"]

@st.cache_data(ttl=600)
def get_dynamic_leaderboard(tickers):
    leaderboard = []
    data = yf.download(tickers, period="2d", interval="1d", group_by='ticker', progress=False)
    for t in tickers:
        try:
            hist = data[t]
            if len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                delta = ((current - prev) / prev) * 100
                leaderboard.append({"ticker": t, "price": current, "delta": delta})
        except: continue
    return sorted(leaderboard, key=lambda x: x['delta'], reverse=True)

# 3. SIDEBAR
with st.sidebar:
    st.title("TERMINAL CORE")
    st.subheader("TOP PERFORMERS (24H)")
    top_5 = get_dynamic_leaderboard(CANDIDATE_POOL)[:5]
    for item in top_5:
        st.metric(label=item["ticker"], value=f"${item['price']:.2f}", delta=f"{item['delta']:.2f}%")
    st.divider()
    st.markdown("### **LEVEL 2 CLEARANCE**\n* Unlimited Neural Dives\n* Institutional SMAs\n* Risk Matrices")
    st.link_button("UPGRADE ACCESS", "https://buy.stripe.com/test_eVqcN4eUHeDq3J8aSDe3e00", use_container_width=True)
    st.divider()
    is_premium = st.checkbox("🔓 Simulate Pro Access (Dev Mode)", value=False)

# 4. TABS & CONTENT
tab1, tab2, tab3 = st.tabs(["HOME ENGINE", "FREE TERMINAL", "PRO QUANT DESK"])

with tab1:
    st.title("SOAR MARKETS PLATFORM")
    st.markdown("### SYSTEMATIC INTELLIGENCE & MICROSTRUCTURE ANALYTICS")
    st.divider()
    
    st.subheader("OUR OBJECTIVE")
    st.markdown("SOAR MARKETS provides professional-grade market telemetry by seamlessly bridging the gap between sophisticated financial data infrastructure and advanced generative artificial intelligence. Our objective is to equip market participants with high-fidelity analytics, quantitative risk metrics, and accelerated neural synthesis.")
    
    st.write("")
    st.subheader("THE ALPHA ARCHITECTURE: CORE CAPABILITIES")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**1. High-Fidelity Microstructure Data**\nAccess granular market telemetry, including order-flow velocity vectors and advanced asset volatility.")
    with col2:
        with st.container(border=True):
            st.markdown("**2. Contextual Neural Synthesis**\nUtilize our specialized LLM pipelines designed to evaluate macro-economic catalysts into actionable insights.")
    
    st.divider()
    st.subheader("LEVEL 2 CLEARANCE PRIVILEGES")
    col3, col4 = st.columns(2)
    col3.markdown("* **Asymmetric Risk Matrices:** Advanced modeling mapping upside momentum.")
    col4.markdown("* **Technical Breakout Thresholds:** Precision signaling for resistance and support.")
    
    st.link_button("INITIALIZE LEVEL 2 CLEARANCE (PRO UPGRADE)", "https://buy.stripe.com/test_eVqcN4eUHeDq3J8aSDe3e00", use_container_width=True)
    
    st.divider()
    st.caption("**SYSTEMATIC DISCLAIMER:** The data, telemetry, and neural output provided by SOAR MARKETS are for educational, informational, and quantitative research purposes only. This platform does not provide personalized financial, legal, or investment advice.")

with tab2:
    render_free_terminal(get_stock_data_func)

with tab3:
    render_pro_terminal(is_premium, get_stock_data_func)
