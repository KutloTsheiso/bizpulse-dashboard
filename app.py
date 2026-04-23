import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Business Dashboard", page_icon="🚀", layout="wide")

# --- Custom CSS for colorful vibrant theme ---
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }

    /* Title styling */
    .main-title {
        text-align: center;
        font-size: 3em;
        font-weight: 900;
        background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px;
        margin-bottom: 0px;
    }

    .sub-title {
        text-align: center;
        color: #a0aec0;
        font-size: 1.1em;
        margin-bottom: 30px;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        margin: 5px;
    }
    .kpi-card-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(56, 239, 125, 0.4);
        margin: 5px;
    }
    .kpi-card-orange {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 210, 0, 0.4);
        margin: 5px;
    }
    .kpi-card-red {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 65, 108, 0.4);
        margin: 5px;
    }
    .kpi-value {
        font-size: 2em;
        font-weight: 900;
        color: white;
    }
    .kpi-label {
        font-size: 0.9em;
        color: rgba(255,255,255,0.85);
        margin-top: 5px;
    }

    /* Dialogue bubble */
    .bubble {
        position: relative;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 12px 18px;
        color: #f0f0f0;
        font-size: 0.92em;
        margin-bottom: 10px;
        backdrop-filter: blur(10px);
    }
    .bubble::before {
        content: "";
        position: absolute;
        bottom: -12px;
        left: 20px;
        border-width: 12px 8px 0;
        border-style: solid;
        border-color: rgba(255,255,255,0.2) transparent transparent;
    }
    .mascot {
        font-size: 2.5em;
        margin-top: 5px;
        margin-left: 10px;
    }

    /* Section headers */
    .section-header {
        color: #ffd93d;
        font-size: 1.3em;
        font-weight: 700;
        margin: 20px 0 10px 0;
        border-left: 4px solid #ff6b6b;
        padding-left: 10px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGO & TITLE ---
st.markdown("""
<div style='text-align:center; padding: 10px 0;'>
    <div style='font-size:5em;'>📊🚀✨</div>
    <div class='main-title'>BizPulse Dashboard</div>
    <div class='sub-title'>Your business performance at a glance — live, interactive & beautiful</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Load Data ---
df = pd.read_csv("business_data.csv")

# --- Sidebar Filters ---
st.sidebar.markdown("## 🎛️ Filters")
regions = ["All"] + list(df["Region"].unique())
selected_region = st.sidebar.selectbox("🌍 Select Region", regions)
categories = ["All"] + list(df["Category"].unique())
selected_category = st.sidebar.selectbox("🏷️ Select Category", categories)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class='bubble'>💡 Tip: Filter by region or category to explore your data!</div>
<div class='mascot'>🤖</div>
""", unsafe_allow_html=True)

# --- Apply Filters ---
filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

# --- KPI Cards ---
st.markdown("<div class='section-header'>📈 Key Metrics</div>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-value'>R{filtered_df['Sales'].sum():,}</div>
        <div class='kpi-label'>💰 Total Sales</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class='kpi-card-red'>
        <div class='kpi-value'>R{filtered_df['Expenses'].sum():,}</div>
        <div class='kpi-label'>💸 Total Expenses</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class='kpi-card-green'>
        <div class='kpi-value'>R{filtered_df['Profit'].sum():,}</div>
        <div class='kpi-label'>🏆 Total Profit</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class='kpi-card-orange'>
        <div class='kpi-value'>{filtered_df['Units_Sold'].sum():,}</div>
        <div class='kpi-label'>📦 Units Sold</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Row 1: Line Chart & Bubble Insight ---
st.markdown("<div class='section-header'>📉 Monthly Trends</div>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    fig1 = px.line(filtered_df, x="Month", y=["Sales", "Expenses", "Profit"],
                   markers=True,
                   color_discrete_map={"Sales": "#4d96ff", "Expenses": "#ff6b6b", "Profit": "#6bcb77"},
                   labels={"value": "Amount (R)", "variable": "Category"},
                   template="plotly_dark")
    fig1.update_traces(line=dict(width=3))
    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="white")),
        font=dict(color="white"),
        transition_duration=500)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    best_month = filtered_df.loc[filtered_df["Sales"].idxmax(), "Month"]
    best_sales = filtered_df["Sales"].max()
    avg_profit = int(filtered_df["Profit"].mean())
    st.markdown(f"""
    <div class='bubble'>🏆 <b>{best_month}</b> was your best month with <b>R{best_sales:,}</b> in sales!</div>
    <div class='mascot'>🦸</div>
    <br>
    <div class='bubble'>📊 Your average monthly profit is <b>R{avg_profit:,}</b>. Keep it up!</div>
    <div class='mascot'>🤩</div>
    """, unsafe_allow_html=True)

# --- Row 2: Bar Chart & Bubble Insight ---
st.markdown("<div class='section-header'>📦 Units Sold</div>", unsafe_allow_html=True)
col3, col4 = st.columns([1, 3])

with col3:
    best_units_month = filtered_df.loc[filtered_df["Units_Sold"].idxmax(), "Month"]
    best_units = filtered_df["Units_Sold"].max()
    total_units = filtered_df["Units_Sold"].sum()
    st.markdown(f"""
    <div class='bubble'>🚀 <b>{best_units_month}</b> had the most units sold: <b>{best_units:,}</b> units!</div>
    <div class='mascot'>😎</div>
    <br>
    <div class='bubble'>📦 You sold a total of <b>{total_units:,}</b> units this year. Impressive!</div>
    <div class='mascot'>🎉</div>
    """, unsafe_allow_html=True)

with col4:
    fig2 = px.bar(filtered_df, x="Month", y="Units_Sold",
                  color="Units_Sold",
                  color_continuous_scale=["#4d96ff", "#ffd93d", "#ff6b6b"],
                  labels={"Units_Sold": "Units Sold"},
                  template="plotly_dark")
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(color="white"),
        transition_duration=500)
    st.plotly_chart(fig2, use_container_width=True)

# --- Row 3: Pie Chart & Scatter Plot ---
st.markdown("<div class='section-header'>🔍 Deep Dive</div>", unsafe_allow_html=True)
col5, col6 = st.columns(2)

with col5:
    category_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    top_category = category_sales.loc[category_sales["Sales"].idxmax(), "Category"]
    fig3 = px.pie(category_sales, values="Sales", names="Category",
                  hole=0.4,
                  color_discrete_sequence=["#4d96ff", "#ff6b6b", "#6bcb77"],
                  template="plotly_dark")
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        transition_duration=500)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown(f"""
    <div class='bubble'>🥇 <b>{top_category}</b> is your top performing category!</div>
    <div class='mascot'>🏅</div>
    """, unsafe_allow_html=True)

with col6:
    fig4 = px.scatter(filtered_df, x="Units_Sold", y="Sales",
                      color="Region",
                      size="Profit",
                      hover_data=["Month"],
                      color_discrete_sequence=["#4d96ff", "#ff6b6b", "#6bcb77", "#ffd93d"],
                      labels={"Units_Sold": "Units Sold", "Sales": "Sales (R)"},
                      template="plotly_dark")
    fig4.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(color="white"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        transition_duration=500)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown(f"""
    <div class='bubble'>💡 Bigger bubbles = higher profit. Hover over dots to explore!</div>
    <div class='mascot'>🔬</div>
    """, unsafe_allow_html=True)

# --- Raw Data Table ---
st.markdown("<div class='section-header'>📄 Raw Data</div>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)

st.markdown("""
<br>
<div style='text-align:center; color: rgba(255,255,255,0.3); font-size:0.85em;'>
    Built with ❤️ using Python, Streamlit & Plotly
</div>
""", unsafe_allow_html=True)