import streamlit as st
import requests
import pandas as pd

# Terminal Configuration
st.set_page_config(page_title="Alpha-Terminal V1", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for a "Bloomberg" dark-room feel
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { color: #00ff00; font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 ALPHA-TERMINAL SYSTEM")
st.divider()

# Sidebar for the "Top 5" (The Persistent Data)
with st.sidebar:
    st.header("Daily Top 5")
    # Placeholder: We will eventually hook this to your Pipedream 'Top 5' workflow
    st.table({"Ticker": ["NVDA", "TSLA", "AAPL", "MSFT", "AMD"], "Signal": ["BUY", "HOLD", "BUY", "SELL", "BUY"]})

# Main Analysis Interface
col1, col2 = st.columns([1, 2])

with col1:
    ticker = st.text_input("QUERY TICKER:", placeholder="e.g. NVDA").upper()
    analyze_btn = st.button("EXECUTE ANALYSIS")

with col2:
    if analyze_btn and ticker:
        with st.spinner(f"fetching remote telemetry for {ticker}..."):
            try:
                # 1. Pull secret using the LABEL
                PIPEDREAM_URL = st.secrets["PIPEDREAM_URL"] 
                
                # 2. Execute request
                res = requests.post(PIPEDREAM_URL, json={"ticker": ticker}, timeout=45)
                
                # 3. Handle response
                if res.status_code == 200:
                    prediction = res.json().get("prediction")
                    st.success(f"ANALYSIS COMPLETE: {ticker}")
                    st.write(prediction)
                else:
                    st.error(f"SYSTEM ERROR: {res.status_code}")
                    
            except Exception as e:
                st.error(f"CONNECTION FAILURE: {str(e)}")
# Add this to your Sidebar
with st.sidebar:
    st.header("💳 SUBSCRIPTION")
    status = st.radio("Account Type:", ["Free", "Pro (Locked)"])
    if status == "Free":
        st.warning("You are on the Limited Plan.")
        st.button("Upgrade to Pro for $19/mo")                
