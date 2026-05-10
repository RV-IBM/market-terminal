import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import ast

# 1. Page Configuration & Advanced Hexagonal Styling
st.set_page_config(page_title="SOAR MARKETS", layout="wide")

st.markdown("""
    <style>
    /* Hexagonal Background Pattern */
    [data-testid="stAppViewContainer"] {
        background-color: #02060a;
        background-image:
            radial-gradient(circle at center, rgba(0, 242, 255, 0.05) 0%, transparent 80%),
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
        background-attachment: fixed;
    }

    /* Hexagonal Grid Overlay */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: 
            linear-gradient(30deg, #02060a 12%, transparent 12.5%, transparent 87%, #02060a 87.5%, #02060a),
            linear-gradient(-30deg, #02060a 12%, transparent 12.5%, transparent 87%, #02060a 87.5%, #02060a),
            linear-gradient(30deg, #02060a 12%, transparent 12.5%, transparent 87%, #02060a 87.5%, #02060a),
            linear-gradient(-30deg, #02060a 12%, transparent 12.5%, transparent 87%, #02060a 87.5%, #02060a),
            linear-gradient(60deg, rgba(0, 242, 255, 0.02) 25%, transparent 25.5%, transparent 75%, rgba(0, 242, 255, 0.02) 75%, rgba(0, 242, 255, 0.02)),
            linear-gradient(60deg, rgba(0, 242, 255, 0.02) 25%, transparent 25.5%, transparent 75%, rgba(0, 242, 255, 0.02) 75%, rgba(0, 242, 255, 0.02));
        background-size: 80px 140px;
        pointer-events: none;
        z-index: 0;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #010408; 
        border-right: 2px solid #00f2ff;
        box-shadow: 5px 0 15px rgba(0, 242, 255, 0.1);
    }

    /* Glowing Titles */
    h1, h2, h3 { 
        color: #00f2ff; 
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.8); 
        font-family: 'Courier New', monospace; 
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Interactive Metric Boxes with Gradient Edges */
    .stMetric { 
        background: rgba(11, 20, 32, 0.9) !important;
        border: 1px solid rgba(0, 242, 255, 0.2) !important;
        border-radius: 8px !important;
        padding: 20px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stMetric:hover {
        border: 1px solid #00f2ff !important;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
        transform: translateY(-5px);
        background: linear-gradient(145deg, rgba(11, 20, 32, 1), rgba(0, 242, 255, 0.05)) !important;
    }

    /* Synchronized Blue Glow Buttons */
    .stButton>button, [data-testid="stLinkButton"]>a { 
        background: linear-gradient(90deg, #00f2ff, #0072ff) !important; 
        color: #000000 !important; 
        font-weight: 900 !important; 
        width: 100% !important; 
        border: none !important; 
        border-radius: 4px !important;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.5) !important;
        text-decoration: none !important;
        text-align: center !important;
        display: inline-block !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover, [data-testid="stLinkButton"]>a:hover {
        filter: brightness(1.2);
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.8) !important;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Caching with Multi-Key Extraction (Fixes N/A Metrics)
@st.cache_data(ttl=3600)
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    try:
        raw_info = stock.info
    except:
        raw_info = {}
    try:
        fast_info = stock.fast_info
    except:
        fast_info = {}

    # Comprehensive dictionary search to find actual numbers
    info = {
        "marketCap": raw_info.get("marketCap") or fast_info.get("marketCap") or "N/A",
        "volume": raw_info.get("regularMarketVolume") or fast_info.get("lastVolume") or "N/A",
        "fiftyTwoWeekHigh": raw_info.get("fiftyTwoWeekHigh") or fast_info.get("yearHigh") or "N/A",
        "trailingPE": raw_info.get("trailingPE") or "N/A"
    }
    hist = stock.history(period="1mo")
    return info, hist

# 3. Dynamic Leaderboard (Sorted by Change)
CANDIDATE_POOL = ["NVDA", "AAPL", "TSLA", "MSFT", "GOOGL", "AVGO", "META", "AMZN", "PLTR"]

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
            except: continue
        return sorted(leaderboard, key=lambda x: x['delta'], reverse=True)[:5]
    except: return []

# 4. Sidebar UI
with st.sidebar:
    st.title("SOAR CORE")
    st.subheader("TOP GAINERS")
    top_5 = get_dynamic_leaderboard(CANDIDATE_POOL)
    for item in top_5:
        st.metric(label=item["ticker"], value=f"${item['price']:.2f}", delta=f"{item['delta']:.2f}%")

    st.divider()
    st.markdown("### **LEVEL 2 CLEARANCE**\n* Unlimited Neural Dives\n* 30-Day Intelligence")
    st.link_button("UPGRADE ACCESS", "https://buy.stripe.com/your_link", use_container_width=True)

# 5. Main UI
st.title("SOAR MARKETS")

# Top-level Upgrade Button
col_main, col_btn = st.columns([3, 1])
with col_btn:
    st.link_button("UPGRADE ACCESS ", "https://buy.stripe.com/your_link")

ticker = st.text_input("INPUT STOCK PROTOCOL (e.g., NVDA):", placeholder="Enter Ticker...").upper()

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
                        # Robust Decoder for AI dictionary
                        raw = res.json().get("prediction", "")
                        try:
                            if isinstance(raw, str) and "candidates" in raw:
                                data = ast.literal_eval(raw)
                                clean_text = data["candidates"][0]["content"]["parts"][0]["text"]
                            elif isinstance(raw, dict) and "candidates" in raw:
                                clean_text = raw["candidates"][0]["content"]["parts"][0]["text"]
                            else:
                                clean_text = str(raw)
                        except:
                            clean_text = str(raw)
                        st.markdown(clean_text)
                else:
                    st.error("NEURAL LINK FAILURE")

            st.divider()
            
            # Visual Telemetry
            col_chart, col_stats = st.columns([2, 1])
            with col_chart:
                st.subheader(f"📊 {ticker} TREND")
                st.line_chart(hist['Close'])

            with col_stats:
                st.subheader("📑 METRICS")
                def fmt(val, cur=True):
                    if not isinstance(val, (int, float)): return "N/A"
                    return f"${val:,.2f}" if cur else f"{val:,.0f}"
                
                st.write(f"**Market Cap:** {fmt(info['marketCap'])}")
                st.write(f"**P/E Ratio:** {info['trailingPE']}")
                st.write(f"**Volume:** {fmt(info['volume'], False)}")
                st.write(f"**52W High:** {fmt(info['fiftyTwoWeekHigh'])}")

        except Exception as e:
            st.error(f"CRITICAL ERROR: {str(e)}")
