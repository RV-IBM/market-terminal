import streamlit as st
import requests
import ast

def render_free_terminal(get_stock_data_func):
    st.title("📡 STANDARD INTELLIGENCE STREAM")
    ticker = st.text_input("INPUT STOCK PROTOCOL (FREE TIER):", placeholder="e.g., NVDA, AMD").upper()
    
    if st.button("EXECUTE NEURAL DIVE"):
        if ticker:
            try:
                info, hist = get_stock_data_func(ticker, range_type="free")
               with st.spinner("Decoding Neural Telemetry..."):
        url = st.secrets["PIPEDREAM_URL"]
        
        try:
            # 45s timeout catches the delay before Pipedream's 60s hard crash
            res = requests.post(url, json={"ticker": ticker, "tier": "free"}, timeout=45)
            
            if res.status_code == 200:
                st.success("📡 NEURAL LINK ESTABLISHED")
                with st.container(border=True):
                    raw_prediction = res.json().get("prediction", "No telemetry data.")
                    try:
                        if isinstance(raw_prediction, str) and "candidates" in raw_prediction:
                            import ast
                            parsed_dict = ast.literal_eval(raw_prediction)
                            clean_output = parsed_dict["candidates"][0]["content"]["parts"][0]["text"]
                        else: 
                            clean_output = str(raw_prediction)
                    except: 
                        clean_output = str(raw_prediction)
                    st.markdown(clean_output)
            else: 
                st.error("NEURAL LINK FAILURE")
                
        except requests.exceptions.Timeout:
            st.warning("📡 TELEMETRY DELAY: Processing took longer than 45 seconds. Please click again to retry the payload.")
        except requests.exceptions.RequestException:
            st.error("⚠️ PIPELINE ERROR: Interface gateway disconnected. Please check your network connection.")
                
                st.divider()
                col_chart, col_stats = st.columns([2, 1])
                with col_chart:
                    st.subheader(f"📊 {ticker} 30-DAY TREND")
                    if not hist.empty: st.line_chart(hist['Close'])
                with col_stats:
                    st.subheader("📝 KEY METRICS")
                    st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
                    st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
                    st.write(f"**Volume:** {info.get('volume', 'N/A')}")
                    st.write(f"**52 Week High:** {info.get('fiftyTwoWeekHigh', 'N/A')}")
            except Exception as e: st.error(f"SYSTEM CRASH: {str(e)}")
        else: st.warning("PLEASE INPUT A TICKER.")
