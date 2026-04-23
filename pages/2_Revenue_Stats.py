import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Revenue Stats", page_icon="💰", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    .page-title {
        text-align: center;
        font-size: 2.8em;
        font-weight: 900;
        background: linear-gradient(90deg, #ffd93d, #6bcb77, #4d96ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102,126,234,0.4);
        margin: 5px;
    }
    .kpi-card-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .kpi-card-orange {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .kpi-card-red {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .kpi-value {
        font-size: 1.8em;
        font-weight: 900;
        color: white;
    }
    .kpi-label {
        color: rgba(255,255,255,0.85);
        font-size: 0.9em;
        margin-top: 5px;
    }
    .bubble {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 12px 18px;
        color: #f0f0f0;
        font-size: 0.92em;
        margin-bottom: 10px;
        backdrop-filter: blur(10px);
    }
    .section-header {
        color: #ffd93d;
        font-size: 1.3em;
        font-weight: 700;
        margin: 20px 0 10px 0;
        border-left: 4px solid #6bcb77;
        padding-left: 10px;
    }
    .progress-label {
        color: white;
        font-size: 0.95em;
        margin-bottom: 3px;
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

# --- Title ---
st.markdown("""
<div style='text-align:center; padding: 10px 0;'>
    <div style='font-size:3em;'>💰</div>
    <div class='page-title'>Revenue Stats Dashboard</div>
    <p style='color:#a0aec0; text-align:center;'>Revenue trends, targets, growth and client analysis</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Load Data ---
df = pd.read_csv("data/revenue_stats.csv")

# --- Sidebar Filters ---
st.sidebar.markdown("## 🎛️ Filters")
streams = ["All"] + list(df["Stream"].unique())
selected_stream = st.sidebar.selectbox("💼 Revenue Stream", streams)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class='bubble'>💡 Filter by revenue stream to analyse each income source!</div>
""", unsafe_allow_html=True)

# --- Apply Filters ---
filtered_df = df.copy()
if selected_stream != "All":
    filtered_df = filtered_df[filtered_df["Stream"] == selected_stream]

# --- Calculations ---
total_actual = filtered_df["Actual_Revenue"].sum()
total_target = filtered_df["Target_Revenue"].sum()
total_last_year = filtered_df["Last_Year_Revenue"].sum()
growth = ((total_actual - total_last_year) / total_last_year) * 100
target_achievement = (total_actual / total_target) * 100
total_new_clients = filtered_df["New_Clients"].sum()

# --- KPI Cards ---
st.markdown("<div class='section-header'>📈 Key Metrics</div>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>R{total_actual:,}</div>
        <div class='kpi-label'>💰 Actual Revenue</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-card-green'>
        <div class='kpi-value'>{growth:.1f}%</div>
        <div class='kpi-label'>📈 YoY Growth</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-card-orange'>
        <div class='kpi-value'>{target_achievement:.1f}%</div>
        <div class='kpi-label'>🎯 Target Achievement</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-card-red'>
        <div class='kpi-value'>{total_new_clients}</div>
        <div class='kpi-label'>🤝 New Clients</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Row 1: Actual vs Target vs Last Year ---
st.markdown("<div class='section-header'>🎯 Actual vs Target vs Last Year</div>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=filtered_df["Month"], y=filtered_df["Actual_Revenue"],
                              mode="lines+markers", name="Actual",
                              line=dict(color="#6bcb77", width=3)))
    fig1.add_trace(go.Scatter(x=filtered_df["Month"], y=filtered_df["Target_Revenue"],
                              mode="lines+markers", name="Target",
                              line=dict(color="#ffd93d", width=3, dash="dash")))
    fig1.add_trace(go.Scatter(x=filtered_df["Month"], y=filtered_df["Last_Year_Revenue"],
                              mode="lines+markers", name="Last Year",
                              line=dict(color="#ff6b6b", width=3, dash="dot")))
    fig1.update_layout(template="plotly_dark",
                       paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"),
                       yaxis_title="Revenue (R)",
                       xaxis_title="Month")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    months_above = (filtered_df["Actual_Revenue"] >= filtered_df["Target_Revenue"]).sum()
    st.markdown(f"""
    <div class='bubble'>🎯 Target hit in <b>{months_above}</b> out of <b>{len(filtered_df)}</b> months!</div>
    <br>
    <div class='bubble'>📈 Year on year growth of <b>{growth:.1f}%</b> — great progress!</div>
    <br>
    <div class='bubble'>💰 Revenue is <b>R{total_actual - total_last_year:,}</b> more than last year!</div>
    """, unsafe_allow_html=True)

# --- Row 2: Monthly Growth Rate & Revenue Stream ---
st.markdown("<div class='section-header'>📊 Growth & Revenue Streams</div>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    filtered_df = filtered_df.copy()
    filtered_df["Growth_%"] = filtered_df["Actual_Revenue"].pct_change() * 100
    fig2 = px.bar(filtered_df, x="Month", y="Growth_%",
                  color="Growth_%",
                  color_continuous_scale=["#ff6b6b", "#ffd93d", "#6bcb77"],
                  template="plotly_dark",
                  labels={"Growth_%": "Growth (%)"})
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""<div class='bubble'>📊 Green bars = growth months, Red bars = decline months!</div>""",
                unsafe_allow_html=True)

with col4:
    stream_data = df.groupby("Stream")["Actual_Revenue"].sum().reset_index()
    fig3 = px.pie(stream_data, values="Actual_Revenue", names="Stream",
                  hole=0.4,
                  color_discrete_sequence=["#4d96ff", "#ff6b6b", "#6bcb77"],
                  template="plotly_dark")
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(color="white"))
    st.plotly_chart(fig3, use_container_width=True)
    top_stream = stream_data.loc[stream_data["Actual_Revenue"].idxmax(), "Stream"]
    st.markdown(f"""<div class='bubble'>💼 <b>{top_stream}</b> is the biggest revenue stream!</div>""",
                unsafe_allow_html=True)

# --- Row 3: Client Growth ---
st.markdown("<div class='section-header'>🤝 Client Growth</div>", unsafe_allow_html=True)
col5, col6 = st.columns([3, 1])

with col5:
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=filtered_df["Month"], y=filtered_df["New_Clients"],
                          name="New Clients", marker_color="#4d96ff"))
    fig4.add_trace(go.Bar(x=filtered_df["Month"], y=filtered_df["Recurring_Clients"],
                          name="Recurring Clients", marker_color="#6bcb77"))
    fig4.update_layout(barmode="group",
                       template="plotly_dark",
                       paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"),
                       yaxis_title="Number of Clients")
    st.plotly_chart(fig4, use_container_width=True)

with col6:
    total_recurring = filtered_df["Recurring_Clients"].sum()
    retention = (total_recurring / (total_recurring + total_new_clients)) * 100
    st.markdown(f"""
    <div class='bubble'>🤝 <b>{total_new_clients}</b> new clients acquired this year!</div>
    <br>
    <div class='bubble'>🔄 Client retention rate is <b>{retention:.1f}%</b> — excellent!</div>
    """, unsafe_allow_html=True)

# --- Raw Data ---
st.markdown("<div class='section-header'>📄 Raw Data</div>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)

st.markdown("""
<br><div style='text-align:center; color:rgba(255,255,255,0.3); font-size:0.85em;'>
Kutlo Tsheiso Data Land — Revenue Stats Dashboard
</div>""", unsafe_allow_html=True)