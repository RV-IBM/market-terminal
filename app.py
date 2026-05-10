import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# 1. Page Configuration & Custom Neon Theme
st.set_page_config(page_title="SOAR MARKETS", layout="wide")

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
    
    # We use fast_info here instead of .info to prevent the Too Many Requests error
    try:
        info = {
            "marketCap": stock.fast_info.get("marketCap", "N/A"),
            "volume": stock.fast_info.get("lastVolume", "N/A"),
            "fiftyTwoWeekHigh": stock.fast_info.get("yearHigh", "N/A"),
            # trailingPE isn't in fast_info, so we safely try to grab it from standard info
            "trailingPE": stock.info.get("trailingPE", "N/A") if hasattr(stock, 'info') else "N/A"
        }
    except Exception:
        info = {}
        
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
        # Download data for the entire pool at once
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
                
        # Sort by 'delta' (percentage change) from highest to lowest
        sorted_list = sorted(leaderboard, key=lambda x: x['delta'], reverse=True)
        return sorted_list[:5]
    except Exception:
        # If rate limited, return an empty list instead of crashing
        return []

# 4. Sidebar UI
with st.sidebar:
    st.title("SOAR MARKETS")
    
    st.subheader("TOP PERFORMERS (24H)")
    
    top_5 = get_dynamic_leaderboard(CANDIDATE_POOL)
    
    if not top_5:
        st.warning("RATE LIMIT ACTIVE. Live feed paused to protect system.")
    else:
        for item in top_5:
            st.metric(
                label=item["ticker"], 
                value=f"${item['price']:.2f}", 
                delta=f"{item['delta']:.2f}%"
            )

    st.divider()

    # --- PRO UPGRADE SECTION ---
    st.markdown("""
    ### **LEVEL 2 CLEARANCE**
    * **Unlimited Neural Dives**
    * **30-Day Intelligence Briefings**
    * **Institutional Data Stream**
    
    *Gain the edge the machines have.*
    """)
    
    # Add your Stripe URL here
    st.link_button("UPGRADE ACCESS", "https://buy.stripe.com/test_eVqcN4eUHeDq3J8aSDe3e00", use_container_width=True)
    
    st.divider()
    st.caption("SYSTEM STATUS: ENCRYPTED")

# 5. Main UI
st.title("SOAR MARKETS SYSTEM")

# THE MISSING INPUT RESTORED
ticker = st.text_input("INPUT STOCK PROTOCOL (e.g., NVDA, TSLA, AAPL):", placeholder="Enter Ticker...").upper()

# 6. Execution Logic
if st.button("EXECUTE NEURAL DIVE"):
    if ticker: # Ensures ticker exists
        try:
            # Step A: Fetch Market Data via Cache
            info, hist = get_stock_data(ticker)
            
            # Step B: AI Intelligence Briefing
            with st.spinner("Decoding Neural Telemetry..."):
                url = st.secrets["PIPEDREAM_URL"]
                res = requests.post(url, json={"ticker": ticker}, timeout=60)
                
                if res.status_code == 200:
                    st.success("📡 NEURAL LINK ESTABLISHED")
                    with st.container(border=True):
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
                
                # Format numbers cleanly
                m_cap = info.get('marketCap', 'N/A')
                vol = info.get('volume', 'N/A')
                
                if isinstance(m_cap, (int, float)): m_cap = f"${m_cap:,.0f}"
                if isinstance(vol, (int, float)): vol = f"{vol:,.0f}"

                st.write(f"**Market Cap:** {m_cap}")
                st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
                st.write(f"**Volume:** {vol}")
                
                high_52 = info.get('fiftyTwoWeekHigh', 'N/A')
                if isinstance(high_52, (int, float)): high_52 = f"${high_52:,.2f}"
                st.write(f"**52 Week High:** {high_52}")

        except Exception as e:
            st.error(f"SYSTEM CRASH: {str(e)}")
    else:
        st.warning("PLEASE INPUT A TICKER TO INITIALIZE DIVE.")
