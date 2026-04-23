import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Business Stats", page_icon="📊", layout="wide")

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
        background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77);
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
        box-shadow: 0 8px 32px rgba(56,239,125,0.4);
        margin: 5px;
    }
    .kpi-card-orange {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255,210,0,0.4);
        margin: 5px;
    }
    .kpi-card-red {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255,65,108,0.4);
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
        border-left: 4px solid #ff6b6b;
        padding-left: 10px;
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
    <div style='font-size:3em;'>📊</div>
    <div class='page-title'>Business Stats Dashboard</div>
    <p style='color:#a0aec0; text-align:center;'>Overall business performance across South Africa</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Load Data ---
df = pd.read_csv("data/business_stats.csv")

# --- Sidebar Filters ---
st.sidebar.markdown("## 🎛️ Filters")
regions = ["All"] + list(df["Region"].unique())
selected_region = st.sidebar.selectbox("🌍 Select Region", regions)
teams = ["All"] + list(df["Team"].unique())
selected_team = st.sidebar.selectbox("👥 Select Team", teams)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class='bubble'>💡 Filter by region or team to explore performance!</div>
""", unsafe_allow_html=True)

# --- Apply Filters ---
filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]
if selected_team != "All":
    filtered_df = filtered_df[filtered_df["Team"] == selected_team]

# --- KPI Cards ---
st.markdown("<div class='section-header'>📈 Key Metrics</div>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

profit_margin = (filtered_df['Profit'].sum() / filtered_df['Sales'].sum() * 100)

with k1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>R{filtered_df['Sales'].sum():,}</div>
        <div class='kpi-label'>💰 Total Sales</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-card-red'>
        <div class='kpi-value'>R{filtered_df['Expenses'].sum():,}</div>
        <div class='kpi-label'>💸 Total Expenses</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-card-green'>
        <div class='kpi-value'>R{filtered_df['Profit'].sum():,}</div>
        <div class='kpi-label'>🏆 Total Profit</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-card-orange'>
        <div class='kpi-value'>{profit_margin:.1f}%</div>
        <div class='kpi-label'>📊 Profit Margin</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Row 1: Line Chart & Insight ---
st.markdown("<div class='section-header'>📉 Monthly Performance</div>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    fig1 = px.line(filtered_df, x="Month",
                   y=["Sales", "Expenses", "Profit"],
                   markers=True,
                   color_discrete_map={"Sales": "#4d96ff", "Expenses": "#ff6b6b", "Profit": "#6bcb77"},
                   labels={"value": "Amount (R)", "variable": "Metric"},
                   template="plotly_dark")
    fig1.update_traces(line=dict(width=3))
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    best_month = filtered_df.loc[filtered_df["Sales"].idxmax(), "Month"]
    best_sales = filtered_df["Sales"].max()
    avg_profit = int(filtered_df["Profit"].mean())
    st.markdown(f"""
    <div class='bubble'>🏆 <b>{best_month}</b> was the best month with <b>R{best_sales:,}</b> in sales!</div>
    <br>
    <div class='bubble'>📊 Average monthly profit is <b>R{avg_profit:,}</b></div>
    <br>
    <div class='bubble'>💹 Overall profit margin is <b>{profit_margin:.1f}%</b></div>
    """, unsafe_allow_html=True)

# --- Row 2: Regional & Team Performance ---
st.markdown("<div class='section-header'>🌍 Regional & Team Performance</div>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    region_data = df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
    fig2 = px.bar(region_data, x="Region", y=["Sales", "Profit"],
                  barmode="group",
                  color_discrete_map={"Sales": "#4d96ff", "Profit": "#6bcb77"},
                  template="plotly_dark",
                  labels={"value": "Amount (R)", "variable": "Metric"})
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig2, use_container_width=True)
    top_region = region_data.loc[region_data["Sales"].idxmax(), "Region"]
    st.markdown(f"""<div class='bubble'>🌍 <b>{top_region}</b> is the top performing region!</div>""",
                unsafe_allow_html=True)

with col4:
    team_data = df.groupby("Team")[["Sales", "Profit"]].sum().reset_index()
    fig3 = px.pie(team_data, values="Sales", names="Team",
                  hole=0.4,
                  color_discrete_sequence=["#4d96ff", "#ff6b6b", "#6bcb77"],
                  template="plotly_dark")
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(color="white"))
    st.plotly_chart(fig3, use_container_width=True)
    top_team = team_data.loc[team_data["Sales"].idxmax(), "Team"]
    st.markdown(f"""<div class='bubble'>🏅 Team <b>{top_team}</b> leads in total sales!</div>""",
                unsafe_allow_html=True)

# --- Row 3: Expenses vs Profit Scatter ---
st.markdown("<div class='section-header'>🔍 Expenses vs Profit Analysis</div>", unsafe_allow_html=True)
col5, col6 = st.columns([3, 1])

with col5:
    fig4 = px.scatter(filtered_df, x="Expenses", y="Profit",
                      color="Region", size="Sales",
                      hover_data=["Month"],
                      color_discrete_sequence=["#4d96ff", "#ff6b6b", "#6bcb77", "#ffd93d", "#ce93d8"],
                      template="plotly_dark",
                      labels={"Expenses": "Expenses (R)", "Profit": "Profit (R)"})
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig4, use_container_width=True)

with col6:
    st.markdown("""
    <div class='bubble'>💡 Bigger bubbles = higher sales. Look for months with low expenses but high profit!</div>
    <br>
    <div class='bubble'>🎯 Hover over any bubble to see the month details!</div>
    """, unsafe_allow_html=True)

# --- Raw Data ---
st.markdown("<div class='section-header'>📄 Raw Data</div>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)

st.markdown("""
<br><div style='text-align:center; color:rgba(255,255,255,0.3); font-size:0.85em;'>
Kutlo Tsheiso Data Land — Business Stats Dashboard
</div>""", unsafe_allow_html=True)