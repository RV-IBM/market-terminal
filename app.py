import streamlit as st
import pandas as pd
import yfinance as yf
import requests

@st.cache_data(ttl=3600)
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.info, stock.history(period="1mo")

# --- 1. SETTINGS & NEON THEME ---
st.set_page_config(page_title="SOAR Markets", layout="wide")

# Neon Blue & Dark Slate Styling
st.markdown("""
    <style>
    .main { background-color: #050a10; color: #00f2ff; }
    .stMetric { background-color: #0b1420; border: 1px solid #00f2ff; border-radius: 10px; padding: 15px; box-shadow: 0 0 10px #00f2ff; }
    [data-testid="stSidebar"] { background-color: #03070b; border-right: 1px solid #00f2ff; }
    h1, h2, h3 { color: #00f2ff; text-shadow: 0 0 8px #00f2ff; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #00f2ff; color: black; border-radius: 5px; font-weight: bold; border: none; box-shadow: 0 0 15px #00f2ff; width: 100%; }
    hr { border-top: 1px solid #00f2ff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: LIVE TOP 5 & SUBSCRIPTION ---
# OVERWRITE THIS SECTION IN YOUR app.py
with st.sidebar:
    st.title("TERMINAL CORE")
    for t in ["NVDA", "TSLA", "AAPL", "BTC-USD", "AMD"]:
        try:
            s = yf.Ticker(t)
            price = s.fast_info['last_price']
            prev = s.fast_info['previous_close']
            # Calculate change manually
            delta = ((price - prev) / prev) * 100
            st.metric(t, f"${price:.2f}", f"{delta:.2f}%")
        except Exception as e:
            st.error(f"Error on {t}")
    
    # WORKING PRO LINK
    st.subheader("💎 PRO Subscription")
    st.write("Unlock 0-latency Neural Analysis.")
    st.markdown("""
    - **Unlimited** AI Deep-Dives
    - **Real-time** Neural Signals
    - **Priority** Data Processing
    """)
    # REPLACE URL BELOW WITH YOUR ACTUAL STRIPE LINK
    st.link_button("UPGRADE TO PRO - $19/mo", "https://buy.stripe.com/your_actual_stripe_link_here", use_container_width=True)

# --- 3. MAIN PAGE: DASHBOARD FILLERS ---
st.title("SOAR Markets")
st.link_button("UPGRADE TO PRO - $19/mo", "https://buy.stripe.com/your_actual_stripe_link_here", use_container_width=True)
# Create a top row of stats to fill space
m1, m2, m3, m4 = st.columns(4)
m1.metric("NETWORK STATUS", "ENCRYPTED", "STABLE")
m2.metric("TOTAL VOLUME", "12.4B", "+2.1%")
m3.metric("BTC DOMINANCE", "52.4%", "UP")
m4.metric("SYSTEM LATENCY", "142ms", "-12ms")

st.divider()

if st.button("EXECUTE NEURAL DIVE"):
    if ticker: # Ensure this matches your text_input variable name
        try:
            # Fetch data using the cache
            info, hist = get_stock_data(ticker)
            
            # AI Analysis Section
            with st.spinner("Decrypting Neural Data..."):
                url = st.secrets["PIPEDREAM_URL"]
                res = requests.post(url, json={"ticker": ticker}, timeout=60)
                if res.status_code == 200:
                    st.success("TELEMETRY DECODED")
                    st.markdown(res.json().get("prediction", "No data returned."))


        
            col_chart, col_stats = st.columns([2, 1])
            with col_chart:
                st.subheader(f"📊 {ticker} TREND")
                st.line_chart(hist['Close'])

            with col_stats:
                st.subheader("📑 KEY METRICS")
                # Safety checks for metrics
                st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
                st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
                st.write(f"**Volume:** {info.get('volume', 'N/A')}")
                
        except Exception as e:
            st.error(f"NEURAL LINK FAILURE: {str(e)}")
