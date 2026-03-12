import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="mySTOCK", layout="wide")

# Custom CSS for a terminal-like feel
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (MARKET LEADERS & PRO UPGRADE) ---
with st.sidebar:
    st.title("Market Leaders")
    st.metric(label="NVDA", value="$822.79", delta="3.2%")
    st.metric(label="TSLA", value="$175.34", delta="-1.1%")
    
    st.divider()
    
    st.header("🚀 Upgrade to Pro")
    st.write("Unlock unlimited searches & priority analysis.")
    if st.button("Get Pro Access - $19/mo", type="primary"):
        st.write("Redirecting to secure payment...")
        # Add your Stripe Payment Link here

# --- 3. MAIN INTERFACE ---
st.title("mySTOCK")
ticker = st.text_input("ENTER TICKER SYSTEM (e.g., NVDA, AAPL, BTC-USD):").upper()

if st.button("EXECUTE DEEP-DIVE"):
    if ticker:
        # --- 4. PRICE CHARTING ---
        st.subheader(f" {ticker} PERFORMANCE (LAST 30 DAYS)")
        try:
            data = yf.download(ticker, period="1mo", interval="1d")
            if not data.empty:
                st.line_chart(data['Close'])
            else:
                st.error("TELEMETRY ERROR: TICKER NOT FOUND.")
        except Exception as e:
            st.error(f"CHARTING ERROR: {str(e)}")

        # --- 5. AI ANALYSIS ---
        with st.spinner(f"Initiating AI Neural Analysis for {ticker}..."):
            try:
                # Always use st.secrets; never hardcode URLs in your script
                PIPEDREAM_URL = st.secrets["PIPEDREAM_URL"]
                
                # Timeout set to 60s to accommodate AI processing time
                res = requests.post(PIPEDREAM_URL, json={"ticker": ticker}, timeout=60)
                
                if res.status_code == 200:
                    prediction = res.json().get("prediction", "No analysis returned.")
                    st.success(f"ANALYSIS COMPLETE: {ticker}")
                    st.markdown(f"### 🤖 AI Market Intelligence")
                    st.write(prediction)
                else:
                    st.error(f"AI SYSTEM OFFLINE: Error {res.status_code}")
            except Exception as e:
                st.error(f"REMOTE CONNECTION FAILURE: {str(e)}")
    else:
        st.warning("PLEASE ENTER A VALID TICKER TO BEGIN.")
