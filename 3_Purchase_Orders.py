import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Purchase Orders", page_icon="📋", layout="wide")

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
        background: linear-gradient(90deg, #4d96ff, #ce93d8, #ff6b6b);
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
        border-left: 4px solid #4d96ff;
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
    <div style='font-size:3em;'>📋</div>
    <div class='page-title'>Purchase Orders Dashboard</div>
    <p style='color:#a0aec0; text-align:center;'>Supplier orders, delivery performance and procurement analysis</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Load Data ---
df = pd.read_csv("data/purchase_orders.csv")

# --- Sidebar Filters ---
st.sidebar.markdown("## 🎛️ Filters")
suppliers = ["All"] + list(df["Supplier"].unique())
selected_supplier = st.sidebar.selectbox("🏭 Select Supplier", suppliers)
statuses = ["All"] + list(df["Status"].unique())
selected_status = st.sidebar.selectbox("📦 Order Status", statuses)
categories = ["All"] + list(df["Category"].unique())
selected_category = st.sidebar.selectbox("🏷️ Category", categories)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class='bubble'>💡 Filter by supplier, status or category to drill down!</div>
""", unsafe_allow_html=True)

# --- Apply Filters ---
filtered_df = df.copy()
if selected_supplier != "All":
    filtered_df = filtered_df[filtered_df["Supplier"] == selected_supplier]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Status"] == selected_status]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

# --- Calculations ---
total_orders = len(filtered_df)
total_value = filtered_df["Order_Value"].sum()
delivered = len(filtered_df[filtered_df["Status"] == "Delivered"])
delayed = len(filtered_df[filtered_df["Status"] == "Delayed"])
pending = len(filtered_df[filtered_df["Status"] == "Pending"])
delivery_rate = (delivered / total_orders * 100) if total_orders > 0 else 0

# --- KPI Cards ---
st.markdown("<div class='section-header'>📈 Key Metrics</div>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{total_orders}</div>
        <div class='kpi-label'>📋 Total Orders</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-card-green'>
        <div class='kpi-value'>R{total_value:,}</div>
        <div class='kpi-label'>💰 Total Order Value</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-card-orange'>
        <div class='kpi-value'>{delivery_rate:.1f}%</div>
        <div class='kpi-label'>✅ Delivery Rate</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-card-red'>
        <div class='kpi-value'>{delayed}</div>
        <div class='kpi-label'>⚠️ Delayed Orders</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Row 1: Order Status & Supplier Performance ---
st.markdown("<div class='section-header'>📊 Order Status & Supplier Performance</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    status_data = df["Status"].value_counts().reset_index()
    status_data.columns = ["Status", "Count"]
    fig1 = px.pie(status_data, values="Count", names="Status",
                  hole=0.4,
                  color="Status",
                  color_discrete_map={"Delivered": "#6bcb77",
                                      "Delayed": "#ffd93d",
                                      "Pending": "#ff6b6b"},
                  template="plotly_dark")
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(color="white"))
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(f"""
    <div class='bubble'>✅ <b>{delivered}</b> delivered, ⚠️ <b>{delayed}</b> delayed, 🕐 <b>{pending}</b> pending</div>
    """, unsafe_allow_html=True)

with col2:
    supplier_data = df.groupby("Supplier")["Order_Value"].sum().reset_index()
    supplier_data = supplier_data.sort_values("Order_Value", ascending=True)
    fig2 = px.bar(supplier_data, x="Order_Value", y="Supplier",
                  orientation="h",
                  color="Order_Value",
                  color_continuous_scale=["#4d96ff", "#ce93d8", "#ff6b6b"],
                  template="plotly_dark",
                  labels={"Order_Value": "Total Order Value (R)"})
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig2, use_container_width=True)
    top_supplier = supplier_data.loc[supplier_data["Order_Value"].idxmax(), "Supplier"]
    st.markdown(f"""
    <div class='bubble'>🏭 <b>{top_supplier}</b> has the highest total order value!</div>
    """, unsafe_allow_html=True)

# --- Row 2: Orders by Category & Region ---
st.markdown("<div class='section-header'>🏷️ Category & Regional Breakdown</div>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    category_data = df.groupby("Category")["Order_Value"].sum().reset_index()
    fig3 = px.bar(category_data, x="Category", y="Order_Value",
                  color="Order_Value",
                  color_continuous_scale=["#4d96ff", "#6bcb77", "#ffd93d"],
                  template="plotly_dark",
                  labels={"Order_Value": "Total Value (R)"})
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig3, use_container_width=True)
    top_category = category_data.loc[category_data["Order_Value"].idxmax(), "Category"]
    st.markdown(f"""
    <div class='bubble'>🏷️ <b>{top_category}</b> has the highest procurement spend!</div>
    """, unsafe_allow_html=True)

with col4:
    region_data = df.groupby("Region")["Order_Value"].sum().reset_index()
    fig4 = px.pie(region_data, values="Order_Value", names="Region",
                  hole=0.4,
                  color_discrete_sequence=["#4d96ff", "#ff6b6b", "#6bcb77", "#ffd93d"],
                  template="plotly_dark")
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(color="white"))
    st.plotly_chart(fig4, use_container_width=True)
    top_region = region_data.loc[region_data["Order_Value"].idxmax(), "Region"]
    st.markdown(f"""
    <div class='bubble'>🌍 <b>{top_region}</b> accounts for the most procurement spend!</div>
    """, unsafe_allow_html=True)

# --- Row 3: Order Value Scatter ---
st.markdown("<div class='section-header'>🔍 Order Value Analysis</div>", unsafe_allow_html=True)
col5, col6 = st.columns([3, 1])

with col5:
    fig5 = px.scatter(filtered_df, x="Order_ID", y="Order_Value",
                      color="Status",
                      size="Order_Value",
                      hover_data=["Supplier", "Category"],
                      color_discrete_map={"Delivered": "#6bcb77",
                                          "Delayed": "#ffd93d",
                                          "Pending": "#ff6b6b"},
                      template="plotly_dark",
                      labels={"Order_Value": "Order Value (R)"})
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    avg_order = int(filtered_df["Order_Value"].mean())
    max_order = filtered_df["Order_Value"].max()
    st.markdown(f"""
    <div class='bubble'>💰 Average order value is <b>R{avg_order:,}</b></div>
    <br>
    <div class='bubble'>🏆 Largest single order is <b>R{max_order:,}</b></div>
    <br>
    <div class='bubble'>💡 Hover over bubbles to see supplier and category details!</div>
    """, unsafe_allow_html=True)

# --- Raw Data Table ---
st.markdown("<div class='section-header'>📄 Raw Data</div>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)

st.markdown("""
<br><div style='text-align:center; color:rgba(255,255,255,0.3); font-size:0.85em;'>
Kutlo Tsheiso Data Land — Purchase Orders Dashboard
</div>""", unsafe_allow_html=True)