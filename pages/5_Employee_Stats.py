import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import os

# --- Page Config ---
st.set_page_config(page_title="Employee Stats", page_icon="👥", layout="wide")

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
        background: linear-gradient(90deg, #4d96ff, #ce93d8, #6bcb77);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px; padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102,126,234,0.4);
        margin: 5px;
    }
    .kpi-card-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 15px; padding: 20px;
        text-align: center; margin: 5px;
    }
    .kpi-card-orange {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        border-radius: 15px; padding: 20px;
        text-align: center; margin: 5px;
    }
    .kpi-card-red {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        border-radius: 15px; padding: 20px;
        text-align: center; margin: 5px;
    }
    .kpi-value { font-size: 1.8em; font-weight: 900; color: white; }
    .kpi-label { color: rgba(255,255,255,0.85); font-size: 0.9em; margin-top: 5px; }
    .bubble {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px; padding: 12px 18px;
        color: #f0f0f0; font-size: 0.92em;
        margin-bottom: 10px;
    }
    .section-header {
        color: #ffd93d; font-size: 1.3em; font-weight: 700;
        margin: 20px 0 10px 0;
        border-left: 4px solid #4d96ff;
        padding-left: 10px;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] * { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("""
<div style='text-align:center; padding: 10px 0;'>
    <div style='font-size:3em;'>👥</div>
    <div class='page-title'>Employee Stats Dashboard</div>
    <p style='color:#a0aec0; text-align:center;'>Live data pulled directly from a SQL database</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Auto create DB if it doesn't exist ---
def create_database():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Employees (
        employee_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT,
        department TEXT, salary REAL, city TEXT, hire_date TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Sales (
        sale_id INTEGER PRIMARY KEY, employee_id INTEGER,
        product TEXT, amount REAL, sale_date TEXT, region TEXT)""")
    employees = [
        (1,"Thabo","Nkosi","Sales",35000,"Johannesburg","2021-03-15"),
        (2,"Lerato","Dlamini","Marketing",42000,"Cape Town","2020-07-01"),
        (3,"Sipho","Mokoena","IT",55000,"Pretoria","2019-11-20"),
        (4,"Zanele","Khumalo","Sales",38000,"Durban","2022-01-10"),
        (5,"Bongani","Zulu","Finance",48000,"Johannesburg","2020-05-25"),
        (6,"Nomsa","Sithole","IT",52000,"Cape Town","2021-08-14"),
        (7,"Mpho","Molefe","Sales",33000,"Pretoria","2023-02-28"),
        (8,"Ayanda","Ndlovu","Marketing",45000,"Durban","2019-06-30"),
        (9,"Kagiso","Mahlangu","Finance",51000,"Johannesburg","2022-09-05"),
        (10,"Thandeka","Mthembu","IT",58000,"Pretoria","2018-12-01"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO Employees VALUES (?,?,?,?,?,?,?)", employees)
    sales = [
        (1,1,"Laptop",15000,"2024-01-05","Gauteng"),
        (2,4,"Phone",8500,"2024-01-12","KZN"),
        (3,7,"Tablet",6200,"2024-01-18","Gauteng"),
        (4,1,"Laptop",15000,"2024-02-03","Gauteng"),
        (5,4,"TV",12000,"2024-02-14","KZN"),
        (6,7,"Phone",8500,"2024-02-22","Western Cape"),
        (7,1,"Headphones",3500,"2024-03-08","Gauteng"),
        (8,4,"Laptop",15000,"2024-03-15","KZN"),
        (9,7,"Tablet",6200,"2024-03-25","Western Cape"),
        (10,1,"TV",12000,"2024-04-02","Gauteng"),
        (11,4,"Headphones",3500,"2024-04-18","KZN"),
        (12,7,"Laptop",15000,"2024-04-28","Gauteng"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO Sales VALUES (?,?,?,?,?,?)", sales)
    conn.commit()
    conn.close()

create_database()

# --- Load data using SQL queries ---
conn = sqlite3.connect("employees.db")

df_employees = pd.read_sql_query("SELECT * FROM Employees", conn)

df_dept = pd.read_sql_query("""
    SELECT department,
           COUNT(*) as headcount,
           ROUND(AVG(salary), 2) as avg_salary,
           SUM(salary) as total_salary
    FROM Employees GROUP BY department
    ORDER BY avg_salary DESC
""", conn)

df_performance = pd.read_sql_query("""
    SELECT e.first_name || ' ' || e.last_name as full_name,
           e.department, e.salary,
           COUNT(s.sale_id) as total_sales,
           ROUND(COALESCE(SUM(s.amount), 0), 2) as total_revenue,
           CASE
               WHEN SUM(s.amount) >= 40000 THEN 'Top Performer'
               WHEN SUM(s.amount) >= 20000 THEN 'Good Performer'
               ELSE 'Needs Improvement'
           END as rating
    FROM Employees e
    LEFT JOIN Sales s ON e.employee_id = s.employee_id
    GROUP BY e.employee_id
    ORDER BY total_revenue DESC
""", conn)

df_region = pd.read_sql_query("""
    SELECT region,
           COUNT(*) as total_sales,
           ROUND(SUM(amount), 2) as total_amount
    FROM Sales GROUP BY region
    ORDER BY total_amount DESC
""", conn)

df_products = pd.read_sql_query("""
    SELECT product,
           COUNT(*) as times_sold,
           ROUND(SUM(amount), 2) as total_revenue
    FROM Sales GROUP BY product
    ORDER BY total_revenue DESC
""", conn)

conn.close()

# --- Sidebar Filters ---
st.sidebar.markdown("## 🎛️ Filters")
departments = ["All"] + list(df_employees["department"].unique())
selected_dept = st.sidebar.selectbox("🏢 Department", departments)
cities = ["All"] + list(df_employees["city"].unique())
selected_city = st.sidebar.selectbox("🌍 City", cities)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class='bubble'>💡 Data is pulled live from a SQLite database!</div>
""", unsafe_allow_html=True)

# --- Apply Filters ---
filtered_emp = df_employees.copy()
if selected_dept != "All":
    filtered_emp = filtered_emp[filtered_emp["department"] == selected_dept]
if selected_city != "All":
    filtered_emp = filtered_emp[filtered_emp["city"] == selected_city]

# --- KPI Cards ---
st.markdown("<div class='section-header'>📈 Key Metrics</div>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{len(filtered_emp)}</div>
        <div class='kpi-label'>👥 Total Employees</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-card-green'>
        <div class='kpi-value'>R{filtered_emp['salary'].mean():,.0f}</div>
        <div class='kpi-label'>💰 Avg Salary</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-card-orange'>
        <div class='kpi-value'>R{filtered_emp['salary'].max():,}</div>
        <div class='kpi-label'>🏆 Highest Salary</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-card-red'>
        <div class='kpi-value'>R{df_region['total_amount'].sum():,.0f}</div>
        <div class='kpi-label'>💳 Total Sales</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Row 1: Department Stats ---
st.markdown("<div class='section-header'>🏢 Department Analysis</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(df_dept, x="department", y="avg_salary",
                  color="avg_salary",
                  color_continuous_scale=["#4d96ff", "#6bcb77", "#ffd93d"],
                  template="plotly_dark",
                  labels={"avg_salary": "Avg Salary (R)", "department": "Department"})
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig1, use_container_width=True)
    top_dept = df_dept.loc[df_dept["avg_salary"].idxmax(), "department"]
    st.markdown(f"""<div class='bubble'>💰 <b>{top_dept}</b> has the highest average salary!</div>""",
                unsafe_allow_html=True)

with col2:
    fig2 = px.pie(df_dept, values="headcount", names="department",
                  hole=0.4,
                  color_discrete_sequence=["#4d96ff", "#ff6b6b", "#6bcb77", "#ffd93d"],
                  template="plotly_dark")
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(color="white"))
    st.plotly_chart(fig2, use_container_width=True)
    largest_dept = df_dept.loc[df_dept["headcount"].idxmax(), "department"]
    st.markdown(f"""<div class='bubble'>👥 <b>{largest_dept}</b> is the largest department!</div>""",
                unsafe_allow_html=True)

# --- Row 2: Performance & Sales ---
st.markdown("<div class='section-header'>🏆 Performance & Sales</div>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    perf_colors = {"Top Performer": "#6bcb77",
                   "Good Performer": "#ffd93d",
                   "Needs Improvement": "#ff6b6b"}
    bar_colors = [perf_colors.get(r, "#4d96ff") for r in df_performance["rating"]]
    fig3 = px.bar(df_performance, x="full_name", y="total_revenue",
                  color="rating",
                  color_discrete_map=perf_colors,
                  template="plotly_dark",
                  labels={"full_name": "Employee", "total_revenue": "Revenue (R)"})
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig3, use_container_width=True)
    top_performer = df_performance.iloc[0]["full_name"]
    st.markdown(f"""<div class='bubble'>🏆 <b>{top_performer}</b> is the top sales performer!</div>""",
                unsafe_allow_html=True)

with col4:
    fig4 = px.bar(df_products, x="product", y="total_revenue",
                  color="total_revenue",
                  color_continuous_scale=["#4d96ff", "#ce93d8", "#ff6b6b"],
                  template="plotly_dark",
                  labels={"product": "Product", "total_revenue": "Revenue (R)"})
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(255,255,255,0.03)",
                       font=dict(color="white"))
    st.plotly_chart(fig4, use_container_width=True)
    top_product = df_products.iloc[0]["product"]
    st.markdown(f"""<div class='bubble'>📦 <b>{top_product}</b> is the best selling product!</div>""",
                unsafe_allow_html=True)

# --- Row 3: Sales by Region & Employee Table ---
st.markdown("<div class='section-header'>🌍 Regional Sales & Employee Directory</div>",
            unsafe_allow_html=True)
col5, col6 = st.columns(2)

with col5:
    fig5 = px.pie(df_region, values="total_amount", names="region",
                  hole=0.4,
                  color_discrete_sequence=["#4d96ff", "#ff6b6b", "#6bcb77"],
                  template="plotly_dark")
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       font=dict(color="white"))
    st.plotly_chart(fig5, use_container_width=True)
    top_region = df_region.iloc[0]["region"]
    st.markdown(f"""<div class='bubble'>🌍 <b>{top_region}</b> leads in total sales!</div>""",
                unsafe_allow_html=True)

with col6:
    st.markdown("<p style='color:#a0aec0;'>📋 Employee Directory</p>", unsafe_allow_html=True)
    st.dataframe(filtered_emp[["first_name", "last_name", "department",
                                "salary", "city", "hire_date"]],
                 use_container_width=True)

st.markdown("""
<br><div style='text-align:center; color:rgba(255,255,255,0.3); font-size:0.85em;'>
Kutlo Tsheiso Data Land — Employee Stats (SQL Powered)
</div>""", unsafe_allow_html=True)