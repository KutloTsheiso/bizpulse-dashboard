import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(
    page_title="Kutlo Tsheiso Data Land",
    page_icon="🌍",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    .main-title {
        text-align: center;
        font-size: 3.5em;
        font-weight: 900;
        background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff, #ff6b6b);
        background-size: 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px;
    }
    .subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 1.2em;
        margin-bottom: 40px;
    }
    .feature-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: transform 0.3s;
        backdrop-filter: blur(10px);
        margin: 10px;
    }
    .feature-card:hover {
        background: rgba(255,255,255,0.1);
    }
    .feature-icon {
        font-size: 3em;
        margin-bottom: 10px;
    }
    .feature-title {
        color: #ffd93d;
        font-size: 1.2em;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .feature-desc {
        color: #a0aec0;
        font-size: 0.9em;
        line-height: 1.5;
    }
    .welcome-box {
        background: linear-gradient(135deg, rgba(77,150,255,0.2), rgba(107,203,119,0.2));
        border: 1px solid rgba(77,150,255,0.3);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .stat-value {
        font-size: 2em;
        font-weight: 900;
        color: white;
    }
    .stat-label {
        color: rgba(255,255,255,0.85);
        font-size: 0.9em;
    }
    .nav-card {
        background: linear-gradient(135deg, rgba(255,107,107,0.2), rgba(255,217,61,0.2));
        border: 1px solid rgba(255,107,107,0.3);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 5px;
        cursor: pointer;
    }
    .nav-title {
        color: #ff6b6b;
        font-size: 1.1em;
        font-weight: 700;
    }
    .nav-desc {
        color: #a0aec0;
        font-size: 0.85em;
        margin-top: 5px;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGO & TITLE ---
st.markdown("""
<div style='text-align:center; padding: 20px 0 10px 0;'>
    <div style='font-size:5em;'>🌍📊✨</div>
    <div class='main-title'>Kutlo Tsheiso Data Land</div>
    <div class='subtitle'>A comprehensive data analytics portfolio showcasing real business insights</div>
</div>
""", unsafe_allow_html=True)

# --- WELCOME BOX ---
st.markdown("""
<div class='welcome-box'>
    <h2 style='color: #4d96ff; margin-bottom: 10px;'>👋 Welcome to Data Land!</h2>
    <p style='color: #e2e8f0; font-size: 1.05em; line-height: 1.7;'>
        This platform demonstrates advanced data analytics skills using Python, Pandas, Plotly and Streamlit.
        Explore four comprehensive dashboards covering key business areas — each powered by realistic 
        South African business data. Use the <b style='color:#ffd93d;'>sidebar navigation</b> or the 
        cards below to explore each section.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- QUICK STATS ---
st.markdown("<h3 style='color:#ffd93d; text-align:center;'>📈 Portfolio at a Glance</h3>", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown("""<div class='stat-card'>
        <div class='stat-value'>4</div>
        <div class='stat-label'>📊 Dashboards</div>
    </div>""", unsafe_allow_html=True)
with s2:
    st.markdown("""<div class='stat-card'>
        <div class='stat-value'>500+</div>
        <div class='stat-label'>📁 Data Points</div>
    </div>""", unsafe_allow_html=True)
with s3:
    st.markdown("""<div class='stat-card'>
        <div class='stat-value'>20+</div>
        <div class='stat-label'>📉 Chart Types</div>
    </div>""", unsafe_allow_html=True)
with s4:
    st.markdown("""<div class='stat-card'>
        <div class='stat-value'>100%</div>
        <div class='stat-label'>🐍 Python Built</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- FEATURE CARDS ---
st.markdown("<h3 style='color:#ffd93d; text-align:center;'>🗺️ Explore the Dashboards</h3>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>📊</div>
        <div class='feature-title'>Business Stats</div>
        <div class='feature-desc'>Overall business performance including sales, expenses, profit and regional breakdown across South Africa.</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>💰</div>
        <div class='feature-title'>Revenue Stats</div>
        <div class='feature-desc'>Deep dive into revenue streams, monthly growth rates, targets vs actuals and year on year comparisons.</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>📋</div>
        <div class='feature-title'>Purchase Orders</div>
        <div class='feature-desc'>Supplier order tracking, delivery performance, order values and procurement analysis.</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>📦</div>
        <div class='feature-title'>Product Stats</div>
        <div class='feature-desc'>Top performing products, category sales, stock levels and product profitability analysis.</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- ABOUT SECTION ---
st.markdown("""
<div style='background: rgba(255,255,255,0.03); border-radius: 20px; padding: 30px; border: 1px solid rgba(255,255,255,0.08);'>
    <h3 style='color:#6bcb77; text-align:center;'>🛠️ Built With</h3>
    <div style='display:flex; justify-content:center; gap:20px; flex-wrap:wrap; margin-top:15px;'>
        <span style='background:rgba(77,150,255,0.2); color:#4d96ff; padding:8px 20px; border-radius:20px; font-weight:600;'>🐍 Python</span>
        <span style='background:rgba(107,203,119,0.2); color:#6bcb77; padding:8px 20px; border-radius:20px; font-weight:600;'>🐼 Pandas</span>
        <span style='background:rgba(255,107,107,0.2); color:#ff6b6b; padding:8px 20px; border-radius:20px; font-weight:600;'>📊 Plotly</span>
        <span style='background:rgba(255,217,61,0.2); color:#ffd93d; padding:8px 20px; border-radius:20px; font-weight:600;'>🌐 Streamlit</span>
        <span style='background:rgba(156,39,176,0.2); color:#ce93d8; padding:8px 20px; border-radius:20px; font-weight:600;'>🔢 NumPy</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<br>
<div style='text-align:center; color: rgba(255,255,255,0.3); font-size:0.85em;'>
    © 2024 Kutlo Tsheiso Data Land — Built with ❤️ using Python & Streamlit
</div>
""", unsafe_allow_html=True)