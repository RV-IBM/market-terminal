import streamlit as st
import requests
import ast

def render_free_terminal(get_stock_data_func):
    st.title("STANDARD INTELLIGENCE STREAM")
    ticker = st.text_input("INPUT STOCK PROTOCOL (FREE TIER):", placeholder="e.g., NVDA, AMD").upper()

        # ====================================================================
    # BASE NEURAL VERDICT SECTION (For Free/Standard Tier)
    # ====================================================================
    st.divider()
    
    # NOTE: Ensure 'ticker' matches your free script's input variable!
    if st.button("RUN STANDARD NEURAL VERDICT"):
        # Updated range_type to "free"
        info, hist = get_stock_data_func(ticker, range_type="free")
        
        with st.spinner("Decoding Standard Quant Telemetry..."):
            url = st.secrets["PIPEDREAM_URL"]
            
            try:
                # Payload explicitly set to "free" tier
                res = requests.post(url, json={"ticker": ticker, "tier": "free"}, timeout=45)
                
                if res.status_code == 200:
                    st.success("⚡ STANDARD LEVEL NEURAL LINK ESTABLISHED")
                    with st.container(border=True):
                        raw_prediction = res.json().get("prediction", "No telemetry data.")
                        clean_output = ""
                        
                        try:
                            import json
                            
                            # 1. Clean the string if Pipedream sent it wrapped in markdown blocks
                            if isinstance(raw_prediction, str):
                                clean_str = raw_prediction.strip()
                                if clean_str.startswith("```json"):
                                    clean_str = clean_str[7:]
                                elif clean_str.startswith("```"):
                                    clean_str = clean_str[3:]
                                if clean_str.endswith("```"):
                                    clean_str = clean_str[:-3]
                                clean_str = clean_str.strip()
                                
                                # 2. Safely load the JSON using the native json library
                                try:
                                    parsed_dict = json.loads(clean_str)
                                except:
                                    parsed_dict = raw_prediction
                            else:
                                parsed_dict = raw_prediction
                            
                            # 3. Drill down into the payload structure
                            if isinstance(parsed_dict, dict):
                                if "candidates" in parsed_dict and len(parsed_dict["candidates"]) > 0:
                                    candidate = parsed_dict["candidates"][0]
                                    if "content" in candidate and "parts" in candidate["content"]:
                                        clean_output = candidate["content"]["parts"][0]["text"]
                                    elif "text" in candidate:
                                        clean_output = candidate["text"]
                                    else:
                                        clean_output = parsed_dict.get("text", str(parsed_dict))
                                else:
                                    clean_output = parsed_dict.get("text", parsed_dict.get("output", str(raw_prediction)))
                            else:
                                clean_output = str(raw_prediction)
                                
                        except Exception as e:
                            clean_output = str(raw_prediction)
                        
                        # 4. Final text cleanup for Streamlit markdown formatting
                        if isinstance(clean_output, str):
                            clean_output = clean_output.replace("\\n", "\n").replace("\\\"", "\"")
                        
                        st.markdown(clean_output)
                else:
                    st.error("NEURAL LINK FAILURE")
                    
            except requests.exceptions.Timeout:
                st.warning("🦤 TELEMETRY DELAY: Matrix generation took longer than 45 seconds. Please click again to retry.")
            except requests.exceptions.RequestException:
                st.error("⚠️ PIPELINE ERROR: Interface gateway disconnected. Please check your network connection.")
