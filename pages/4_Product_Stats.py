import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Product Stats", page_icon="📦", layout="wide")

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
        background: linear-gradient(90deg, #6bcb77, #4d96ff, #ffd93d);
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
    <div style='font-size:3em;'>📦</div>
    <div class='page-title'>Product Stats Dashboard</div>
    <p style='color:#a0aec0; text-align:center;'>Top products, category performance, stock levels and profitability</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Load Data ---
df = pd.read_csv("data/product_stats.csv")

# --- Sidebar Filters ---
st.sidebar.markdown("## 🎛️ Filters")
categories = ["All"] + list(df["Category"].unique())
selected_category = st.sidebar.selectbox("🏷️ Select Category", categories)
regions = ["All"] + list(df["Region"].unique())
selected_region = st.sidebar.selectbox("🌍 Select Region", regions)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class='bubble'>💡 Filter by category or region to explore product performance!</div>
""", unsafe_allow_html=True)

# --- Apply Filters ---
filtered_df = df.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

# --- Calculations ---
total_revenue = filtered_df["Revenue"].sum()
total_profit = filtered_df["Profit"].sum()
total_units = filtered_df["Units_Sold"].sum()
avg_rating = filtered_df["Rating"].mean()
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

# --- KPI Cards ---
st.markdown("<div class='section-header'>📈 Key Metrics</div>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>R{total_revenue:,}</div>
        <div class='kpi-label'>💰 Total Revenue</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-card-green'>
        <div class='kpi-value'>R{total_profit:,}</div>
        <div class='kpi-label'>🏆 Total Profit</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-card-orange'>
        <div class='kpi-value'>{total_units:,}</div>
        <div class='kpi-label'>📦 Units Sold</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-card-red'>
        <div class='kpi-value'>{avg_rating:.1f} ⭐</div>
        <div class='kpi-label'>😊 Avg Rating</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Row 1: Top 10 Products by Revenue ---
st.markdown("<div class='section-header'>🏆 Top Products by Revenue</div>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    top_products = filtered_df.nlargest(10, "Revenue")
    fig1 = px.bar(top_products, x="Revenue", y="Product",
                  orientation="h",
                  color="Revenue",
                  color_continuous_scale=["#4d96ff", "#6bcb77", "#ffd93d"],
                  template="plotly_dark",
                  labels={"Revenue": "Revenue (R)"})
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"),
                       yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    top_product = filtered_df.loc[filtered_df["Revenue"].idxmax(), "Product"]
    top_revenue = filtered_df["Revenue"].max()
    top_rated = filtered_df.loc[filtered_df["Rating"].idxmax(), "Product"]
    st.markdown(f"""
    <div class='bubble'>🥇 <b>{top_product}</b> is the top revenue product at <b>R{top_revenue:,}</b>!</div>
    <br>
    <div class='bubble'>⭐ <b>{top_rated}</b> has the highest customer rating!</div>
    <br>
    <div class='bubble'>💹 Overall profit margin is <b>{profit_margin:.1f}%</b></div>
    """, unsafe_allow_html=True)

# --- Row 2: Category Performance ---
st.markdown("<div class='section-header'>🏷️ Category Performance</div>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    category_data = df.groupby("Category")[["Revenue", "Profit"]].sum().reset_index()
    fig2 = px.bar(category_data, x="Category",
                  y=["Revenue", "Profit"],
                  barmode="group",
                  color_discrete_map={"Revenue": "#4d96ff", "Profit": "#6bcb77"},
                  template="plotly_dark",
                  labels={"value": "Amount (R)", "variable": "Metric"})
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig2, use_container_width=True)
    top_cat = category_data.loc[category_data["Revenue"].idxmax(), "Category"]
    st.markdown(f"""
    <div class='bubble'>🏷️ <b>{top_cat}</b> is the highest revenue category!</div>
    """, unsafe_allow_html=True)

with col4:
    fig3 = px.pie(category_data, values="Profit", names="Category",
                  hole=0.4,
                  color_discrete_sequence=["#4d96ff", "#ff6b6b", "#6bcb77"],
                  template="plotly_dark")
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(color="white"))
    st.plotly_chart(fig3, use_container_width=True)
    top_profit_cat = category_data.loc[category_data["Profit"].idxmax(), "Category"]
    st.markdown(f"""
    <div class='bubble'>💰 <b>{top_profit_cat}</b> generates the most profit!</div>
    """, unsafe_allow_html=True)

# --- Row 3: Stock Levels & Ratings ---
st.markdown("<div class='section-header'>📦 Stock Levels & Ratings</div>", unsafe_allow_html=True)
col5, col6 = st.columns(2)

with col5:
    stock_df = filtered_df.sort_values("Stock_Level", ascending=True)
    fig4 = px.bar(stock_df, x="Stock_Level", y="Product",
                  orientation="h",
                  color="Stock_Level",
                  color_continuous_scale=["#ff6b6b", "#ffd93d", "#6bcb77"],
                  template="plotly_dark",
                  labels={"Stock_Level": "Units in Stock"})
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig4, use_container_width=True)
    low_stock = filtered_df[filtered_df["Stock_Level"] < 20]
    st.markdown(f"""
    <div class='bubble'>⚠️ <b>{len(low_stock)}</b> products have low stock levels (under 20 units)!</div>
    """, unsafe_allow_html=True)

with col6:
    fig5 = px.scatter(filtered_df, x="Units_Sold", y="Rating",
                      size="Revenue",
                      color="Category",
                      hover_data=["Product"],
                      color_discrete_sequence=["#4d96ff", "#ff6b6b", "#6bcb77"],
                      template="plotly_dark",
                      labels={"Units_Sold": "Units Sold", "Rating": "Customer Rating"})
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown(f"""
    <div class='bubble'>💡 Bigger bubbles = higher revenue. Look for high rated, high selling products!</div>
    """, unsafe_allow_html=True)

# --- Raw Data ---
st.markdown("<div class='section-header'>📄 Raw Data</div>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)

st.markdown("""
<br><div style='text-align:center; color:rgba(255,255,255,0.3); font-size:0.85em;'>
Kutlo Tsheiso Data Land — Product Stats Dashboard
</div>""", unsafe_allow_html=True)