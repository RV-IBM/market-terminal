import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# --- 1. SETTINGS & NEON THEME ---
st.set_page_config(page_title="mySTOCK", layout="wide")

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
    st.subheader("LIVE SECTOR FEED")
    
    top_5 = ["NVDA", "TSLA", "AAPL", "BTC-USD", "AMD"]
    
    for t in top_5:
        # Fast info gives us quick access to prices without heavy loading
        s = yf.Ticker(t)
        price = s.fast_info['last_price']
        change = s.fast_info['year_to_date_return'] * 100
        
        # High-tech buy/sell signaling
        signal = "BUY" if change > 0 else "SELL"
        color = "🟢" if signal == "BUY" else "🔴"
        
        st.metric(label=f"{color} {t} | {signal}", value=f"${price:.2f}", delta=f"{change:.2f}%")
    
    st.divider()
    
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
st.title("mySTOCK")

# Create a top row of stats to fill space
m1, m2, m3, m4 = st.columns(4)
m1.metric("NETWORK STATUS", "ENCRYPTED", "STABLE")
m2.metric("TOTAL VOLUME", "12.4B", "+2.1%")
m3.metric("BTC DOMINANCE", "52.4%", "UP")
m4.metric("SYSTEM LATENCY", "142ms", "-12ms")

st.divider()

# Search Interface
ticker_input = st.text_input("INPUT STOCK (e.g., AAPL):").upper()

if st.button("EXECUTE NEURAL DIVE"):
    if ticker_input:
        col_chart, col_stats = st.columns([2, 1])
        
        with col_chart:
            st.subheader(f" {ticker_input} TREND TELEMETRY")
            hist = yf.download(ticker_input, period="1mo", interval="1d")
            if not hist.empty:
                st.line_chart(hist['Close'])
        
        with col_stats:
            st.subheader(" KEY METRICS")
            info = yf.Ticker(ticker_input).info
            st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
            st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
            st.write(f"**Volume:** {info.get('volume', 'N/A')}")

     # AI Analysis Call (Pipedream)
        with st.spinner("Decrypting Neural Data..."):
            try:
                url = st.secrets["PIPEDREAM_URL"]
                res = requests.post(url, json={"ticker": ticker_input}, timeout=60)
                if res.status_code == 200:
                    st.success("DECODING SUCCESS")
                    st.write(res.json().get("prediction", "No analysis found."))
                else:
                    st.error(f"PIPEDREAM LINK DOWN: {res.status_code}")
            except Exception as e:
                st.error(f"NEURAL CONNECTION FAILURE: {e}")
