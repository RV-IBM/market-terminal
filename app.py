import streamlit as st
import yfinance as yf
from datetime import datetime

# Import the page layouts from your new files
from free_terminal import render_free_terminal
from pro_terminal import render_pro_terminal

# 1. PAGE CONFIG & GLOBAL HEX STYLING
st.set_page_config(page_title="ALPHA-TERMINAL", layout="wide")

st.markdown("""
    <style>
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
    h1, h2, h3 { color: #00f2ff !important; text-shadow: 0 0 8px #00f2ff; font-family: 'Courier New', monospace; text-transform: uppercase;}
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
    /* --- TAB NAVIGATION STYLING --- */
    button[data-baseweb="tab"] {
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
/* FORCE THE TAB LIST TO USE YOUR NEON BLUE */
div[data-baseweb="tab-list"] {
    background-color: transparent !important;
}

/* OVERRIDE THE DEFAULT RED/STREAMLIT ACCENT UNDERLINE */
div[data-baseweb="tab-list"] div[role="presentation"] {
    background-color: #00f2ff !important;
}

/* FORCE THE TEXT COLOR OF THE ACTIVE TAB */
div[data-baseweb="tab-list"] button[aria-selected="true"] {
    color: #00f2ff !important;
    border-bottom: 2px solid #00f2ff !important;
}
    </style>
    """, unsafe_allow_html=True)

# 2. GLOBAL SHARED DATA CACHING
@st.cache_data(ttl=3600)
def get_stock_data(symbol, range_type="free"):
    stock = yf.Ticker(symbol)
    period = "1y" if range_type == "pro" else "1mo"
    return stock.info, stock.history(period=period)

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

# 3. GLOBAL SIDEBAR
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
# Replace your existing st.radio block with this:
tab1, tab2, tab3 = st.tabs(["HOME ENGINE", "FREE TERMINAL", "PRO QUANT DESK"])

with tab1:
    st.title("SOAR MARKETS PLATFORM")
    st.markdown("### SYSTEMATIC INTELLIGENCE & MICROSTRUCTURE ANALYTICS")
    
    st.divider()
    
    st.markdown("""
    **SOAR MARKETS** is a next-generation quantitative analytics interface designed to bridge the gap between institutional-grade market telemetry and decentralized generative AI. 

    We engineer hybrid computational frameworks that ingest raw market microstructure data and synthesize it alongside real-time narrative sentiment. By fusing deterministic mathematical models with advanced neural language processing, we provide our users with an asymmetric edge in modern financial markets.

    ### CORE INFRASTRUCTURE
    * **Algorithmic Telemetry:** Processing real-time volatility, volume footprints, and algorithmic momentum indicators.
    * **Neural Sentiment Synthesis:** Deploying specialized LLMs to decode macro-economic narratives and structural market catalysts.
    * **Systematic Execution Edge:** Translating complex data matrices into clear, actionable risk parameters and breakout thresholds.

    ---
    
    ### INITIALIZE YOUR ENVIRONMENT
    Navigate via the top-level command tabs to access your designated workspace:
    
    * **FREE TERMINAL:** Access foundational 30-day directional asset vectors, standard volume metrics, and raw neural network summaries.
    * **PRO QUANT DESK:** Gain Level 2 Clearance. Track multi-frame institutional indicators ($SMA_{50}$), live structural depth matrices, and dynamic asymmetric risk models.
    """)

with tab2:
    # Everything for your Free Terminal goes here
    render_free_terminal(get_stock_data)

with tab3:
    # Everything for your Pro Terminal goes here
    render_pro_terminal(is_premium, get_stock_data)
