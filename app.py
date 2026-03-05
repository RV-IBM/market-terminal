import streamlit as st
import requests

st.title("Market Terminal 2026")

# 1. The Search Bar
ticker = st.text_input("Enter Stock Ticker (e.g., TSLA):").upper()

if st.button("Analyze"):
    if ticker:
        # 2. Sending input to your Pipedream URL
        payload = {"ticker": ticker}
        response = requests.post("https://eosg30vmismhlpj.m.pipedream.net", json=payload)
        
        # 3. Displaying the AI prediction
        if response.status_code == 200:
            st.success(response.json().get("prediction"))
        else:
            st.error("Analysis failed. Check your connection or ticker.")
