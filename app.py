import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import ast

# 1. Page Configuration & Custom XTX-Style Theme
st.set_page_config(page_title="SOAR MARKETS", layout="wide")

st.markdown("""
    <style>
    /* Institutional Dark Theme + Quant Grid Background */
    [data-testid="stAppViewContainer"] {
        background-color: #02060a;
        background-image: 
            linear-gradient(rgba(0, 242, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 242, 255, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #00f2ff;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #010408; 
        border-right: 1px solid rgba(0, 242, 255, 0.2); 
    }
    
    /* Neon Text & Metrics */
    h1, h2, h3 { 
        color: #00f2ff; 
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.3); 
        font-family: 'Courier New', monospace; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stMetric { 
        background-color: rgba(11, 20, 32, 0.8); 
        border: 1px solid rgba(0, 242, 255, 0.3); 
        border-radius: 4px; 
        padding: 15px; 
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.05);
    }
    
    /* Synchronized Blue Glow Buttons (All Buttons & Links) */
    .stButton>button, [data-testid="stLinkButton"]>a { 
        background-color: #00f2ff !important; 
        color: #000000 !important; 
        font-weight: 900 !important; 
        width: 100% !important; 
        border: none !important; 
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.6) !important;
        text-decoration: none !important;
        text-align: center !important;
        display: inline-block !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover, [data-testid="stLinkButton"]>a:hover {
        background-color: #ffffff !important;
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.9) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Caching with Robust Key Extraction
@st.cache_data(ttl=3600)
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    
    # Attempt to get the heavy info first
    try:
        raw_info = stock.info
    except Exception:
        raw_info = {}
        
    # Attempt to get fast_info as a backup
    try:
        fast_info = stock.fast_info
    except Exception:
        fast_info = {}

    # Cast a wide net for the metrics since YF keys frequently change
    info = {
        "marketCap": raw_info.get("marketCap") or fast_info.get("marketCap") or fast_info.get("market_cap", "N/A"),
        "volume": raw_info.get("volume") or raw_info.get("regularMarketVolume") or fast_info.get("lastVolume", "N/A"),
        "fiftyTwoWeekHigh": raw_info.get("fiftyTwoWeekHigh") or fast_info.get("yearHigh", "N/A"),
        "trailingPE": raw_info.get("trailingPE", "N/A")
    }
        
    hist = stock.history(period="1mo")
    return info, hist

# 3. Dynamic Leaderboard
CANDIDATE_POOL = [
    "NVDA", "AAPL", "TSLA", "MSFT", "GOOGL", "AVGO", "META", 
    "AMZN", "NFLX", "AMD", "SMCI", "ARM", "ORCL", "PLTR"
]

@st.cache_data(ttl=600)
def get_dynamic_leaderboard(tickers):
    leaderboard = []
    try:
        data = yf.download(tickers, period="2d", interval="1d", group_by='ticker', progress=False)
        for t in tickers:
            try:
                hist = data[t]
                if len(hist) >= 2:
                    current = float(hist['Close'].iloc[-1])
                    prev = float(hist['Close'].iloc[-2])
                    delta = ((current - prev) / prev) * 100
                    leaderboard.append({"ticker": t, "price": current, "delta": delta})
            except Exception:
                continue
        sorted_list = sorted(leaderboard, key=lambda x: x['delta'], reverse=True)
        return sorted_list[:5]
    except Exception:
        return []

# 4. Sidebar UI
with st.sidebar:
    st.title("SOAR MARKETS")
    
    st.subheader("TOP PERFORMERS (24H)")
    top_5 = get_dynamic_leaderboard(CANDIDATE_POOL)
    
    if not top_5:
        st.warning("RATE LIMIT ACTIVE. Live feed paused.")
    else:
        for item in top_5:
            st.metric(label=item["ticker"], value=f"${item['price']:.2f}", delta=f"{item['delta']:.2f}%")

    st.divider()

    st.markdown("""
    ### **LEVEL 2 CLEARANCE**
    * **Unlimited Neural Dives**
    * **30-Day Intelligence Briefings**
    * **Institutional Data Stream**
    """)
    
    st.link_button("UPGRADE ACCESS", "https://buy.stripe.com/your_test_link", use_container_width=True)
    st.divider()
    st.caption("SYSTEM STATUS: ENCRYPTED // NODE: SLOUGH, UK")

# 5. Main UI
st.title("SOAR MARKETS SYSTEM")

# Sub-Header Upgrade Button
col_a, col_b = st.columns([3, 1])
with col_b:
    st.link_button("UPGRADE ACCESS ⚡", "https://buy.stripe.com/your_test_link", use_container_width=True)

ticker = st.text_input("INPUT STOCK PROTOCOL (e.g., NVDA, TSLA, AAPL):", placeholder="Enter Ticker...").upper()

# 6. Execution Logic
if st.button("EXECUTE NEURAL DIVE"):
    if ticker: 
        try:
            info, hist = get_stock_data(ticker)
            
            with st.spinner("Decoding Neural Telemetry..."):
                url = st.secrets["PIPEDREAM_URL"]
                res = requests.post(url, json={"ticker": ticker}, timeout=60)
                
                if res.status_code == 200:
                    st.success("📡 NEURAL LINK ESTABLISHED")
                    with st.container(border=True):
                        raw_prediction = res.json().get("prediction", "")
                        
                        # DECODER LOGIC: Extracting the actual text from the AI dictionary
                        try:
                            # If Pipedream sent it as a stringified dictionary, convert it to a real python dictionary
                            if isinstance(raw_prediction, str) and raw_prediction.strip().startswith("{"):
                                parsed_data = ast.literal_eval(raw_prediction)
                            else:
                                parsed_data = raw_prediction
                            
                            # Drill down into the Gemini payload structure to get the text
                            clean_text = parsed_data["candidates"][0]["content"]["parts"][0]["text"]
                        except Exception:
                            # If the structure fails, just print whatever we have so the app doesn't crash
                            clean_text = str(raw_prediction)
                            
                        st.markdown(clean_text)
                else:
                    st.error(f"NEURAL LINK FAILURE: Status {res.status_code}")

            st.divider()

            col_chart, col_stats = st.columns([2, 1])

            with col_chart:
                st.subheader(f"📊 {ticker} 30-DAY TREND")
                if not hist.empty:
                    st.line_chart(hist['Close'])

            with col_stats:
                st.subheader("📑 KEY METRICS")
                
                m_cap = info.get('marketCap', 'N/A')
                vol = info.get('volume', 'N/A')
                high_52 = info.get('fiftyTwoWeekHigh', 'N/A')
                
                if isinstance(m_cap, (int, float)): m_cap = f"${m_cap:,.0f}"
                if isinstance(vol, (int, float)): vol = f"{vol:,.0f}"
                if isinstance(high_52, (int, float)): high_52 = f"${high_52:,.2f}"

                st.write(f"**Market Cap:** {m_cap}")
                st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
                st.write(f"**Volume:** {vol}")
                st.write(f"**52 Week High:** {high_52}")

        except Exception as e:
            st.error(f"SYSTEM CRASH: {str(e)}")
    else:
        st.warning("PLEASE INPUT A TICKER TO INITIALIZE DIVE.")
