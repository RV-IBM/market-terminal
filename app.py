import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# 1. UI Setup
st.set_page_config(page_title="mySTOCK", layout="wide")

# Dark Mode CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar: Top 5 & Pro Subscription
with st.sidebar:
    st.title("💠 TERMINAL CONTROL")
    
    st.subheader("Market Leaders")
    # Quick visual metrics for the sidebar
    col1, col2 = st.columns(2)
    col1.metric("NVDA", "822.79", "3.2%")
    col2.metric("BTC", "67k", "2.1%")
    
    st.divider()
    
    # Pro Subscription Section (Fills the space)
    st.subheader("💎 PRO ACCESS")
    st.info("Institutional-grade intelligence.")
    st.markdown("""
    - ✅ **Unlimited** AI Queries
    - ✅ **Real-time** Data Feeds
    - ✅ **Advanced** Technical Analysis
    - ✅ **Predictions** On Stock Crashes 
    """)
    if st.button("UPGRADE - $19/mo", type="primary", use_container_width=True):
        st.write("Redirecting to Stripe Checkout...")

# 3. Main Dashboard logic
st.title(" mySTOCK ")
ticker = st.text_input("QUERY TICKER (e.g., AAPL, NVDA, TSLA):").upper()

if st.button("EXECUTE ANALYSIS"):
    if ticker:
        # CHARTING (Instant Feedback)
        st.subheader(f" {ticker} Trend Analysis")
        data = yf.download(ticker, period="1mo", interval="1d")
        if not data.empty:
            st.line_chart(data['Close'])
        
        # AI ANALYSIS (Remote Call)
        with st.spinner(f"Contacting remote neural network for {ticker}..."):
            try:
                # Use the secret key name, not the URL
                PIPEDREAM_URL = st.secrets["PIPEDREAM_URL"]
                res = requests.post(PIPEDREAM_URL, json={"ticker": ticker}, timeout=60)
                
                if res.status_code == 200:
                    prediction = res.json().get("prediction", "No analysis found.")
                    st.success("TELEMETRY RECEIVED")
                    st.write(prediction)
                else:
                    st.error(f"PIPEDREAM ERROR: {res.status_code}")
            except Exception as e:
                st.error(f"SYSTEM FAILURE: {str(e)}")
