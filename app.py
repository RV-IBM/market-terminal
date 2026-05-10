import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# 1. Page Configuration & Custom Neon Theme
st.set_page_config(page_title="ALPHA-TERMINAL", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050a10; color: #00f2ff; }
    .stMetric { background-color: #0b1420; border: 1px solid #00f2ff; border-radius: 10px; padding: 15px; }
    [data-testid="stSidebar"] { background-color: #03070b; border-right: 1px solid #00f2ff; }
    h1, h2, h3 { color: #00f2ff; text-shadow: 0 0 8px #00f2ff; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #00f2ff; color: black; font-weight: bold; width: 100%; border: none; box-shadow: 0 0 10px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Caching (Stops the YFRateLimitError)
@st.cache_data(ttl=3600)
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.info, stock.history(period="1mo")

# 3. Sidebar: Terminal Status
with st.sidebar:
    st.title("SOAR MARKETS")
    st.subheader("📡 SYSTEM STATUS")
    st.success("QUANT LINK: ACTIVE")
    st.info("CACHE: ENABLED")
    st.divider()
    st.subheader("💎 PRO FEATURES")
    st.link_button("UPGRADE ACCESS", "https://buy.stripe.com/test_eVqcN4eUHeDq3J8aSDe3e00", use_container_width=True)

# 4. Main UI - Input Step
st.title("SOAR MARKETS")

# THE INPUT STEP (The one you accidentally deleted)
ticker = st.text_input("INPUT STOCK PROTOCOL (e.g., NVDA, TSLA, AAPL):", placeholder="Enter Ticker...").upper()

# 5. Execution Logic
if st.button("EXECUTE NEURAL DIVE"):
    if ticker:
        try:
            # Step A: Fetch Market Data via Cache
            info, hist = get_stock_data(ticker)
            
            # Step B: AI Intelligence Briefing
            with st.spinner("Decoding Neural Telemetry..."):
                url = st.secrets["PIPEDREAM_URL"]
                res = requests.post(url, json={"ticker": ticker}, timeout=60)
                
                if res.status_code == 200:
                    st.success("NEURAL LINK ESTABLISHED")
                    with st.container(border=True):
                        # Extracts the prediction text from the JSON response
                        prediction = res.json().get("prediction", "No telemetry data.")
                        st.markdown(prediction)
                else:
                    st.error(f"NEURAL LINK FAILURE: Status {res.status_code}")

            st.divider()

            # Step C: Visual Telemetry (Charts and Stats)
            col_chart, col_stats = st.columns([2, 1])

            with col_chart:
                st.subheader(f"📊 {ticker} 30-DAY TREND")
                if not hist.empty:
                    st.line_chart(hist['Close'])

            with col_stats:
                st.subheader("📑 KEY METRICS")
                st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
                st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
                st.write(f"**Volume:** {info.get('volume', 'N/A')}")
                st.write(f"**52 Week High:** {info.get('fiftyTwoWeekHigh', 'N/A')}")

        except Exception as e:
            st.error(f"SYSTEM CRASH: {str(e)}")
    else:
        st.warning("PLEASE INPUT A TICKER TO INITIALIZE DIVE.")
