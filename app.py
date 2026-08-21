import streamlit as st
import pandas as pd
import plotly.express as px

# STEP 1: Basic page setup
# This just sets the browser tab title, icon, and layout.
st.set_page_config(
    page_title="Smart Public Transport",
    page_icon="🚌",
    layout="wide"
)

# STEP 2: Load the data
# This reads the CSV file into a table called "df".
# Every chart below is just this table, filtered and grouped
# in different ways.
df = pd.read_csv("APSRTC_Transport_Data.csv")

# Get the unique list of routes, bus types, and months
# so we can use them to fill dropdown menus later.
routes = sorted(df.route.unique())
buses = sorted(df.bus_type.unique())
months = sorted(df.month.unique())

# STEP 3: Sidebar navigation
# This creates the menu on the left with 3 options.
# Whatever the user clicks becomes the "page" variable,
# which decides which section of code runs below.
st.sidebar.title("🚌 Smart Public Transport")

target = st.query_params.get("page")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Dashboard", "ℹ️ About Project"],
    index=1 if target == "dashboard" else 0
)

if page != "📊 Dashboard" and target:
    st.query_params.clear()

# PAGE 1: HOME
# This is just descriptive text and boxes explaining
# what the dashboard can do. No data logic happens here.
if page == "🏠 Home":

    st.title("🚌 Smart Public Transport Performance & Passenger Trend Analysis")

    st.header("Introduction")
    st.write(
        "This project uses real transport data from APSRTC to study how buses, "
        "routes, passengers and revenue perform. The main goal is to turn raw data "
        "into easy-to-understand charts, so patterns like busy routes, high revenue "
        "routes, or areas needing improvement can be spotted quickly."
    )

    st.subheader("What This Dashboard Can Do")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 1. Revenue Analysis")
        st.write("Shows how much revenue each route and bus type is generating. "
                  "Helps you quickly see which routes are earning the most and "
                  "which ones are underperforming.")
    with col2:
        st.markdown("### 2. Passenger Analysis")
        st.write("Looks at how many passengers use each route and bus type. "
                  "Helps identify which services are in high demand and which "
                  "are not.")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### 3. Route Performance")
        st.write("Compares different routes side by side. Makes it easy to "
                  "see which routes are doing well and which ones need "
                  "attention.")
    with col4:
        st.markdown("### 4. Monthly Trends")
        st.write("Tracks how revenue changes from month to month. Useful for "
                  "spotting seasonal patterns, like busy or slow months.")

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("### 5. Bus Type Distribution")
        st.write("Shows how passengers are spread across different bus types. "
                  "Helps understand which bus type people prefer to travel in.")
    with col6:
        st.markdown("### 6. Top 5 Revenue Routes")
        st.write("Lists the five routes that generate the highest revenue. "
                  "Gives a quick snapshot of the best-performing routes.")

# PAGE 2: DASHBOARD
# This is the main page. Each section below follows the
# same pattern:
#   1. Show a dropdown filter
#   2. Filter the data table based on the selection
#   3. Group/summarize the filtered data
#   4. Draw a chart from that summary
elif page == "📊 Dashboard":

    st.title("🚌 Smart Public Transport Dashboard")
    
    # ---------- Top KPI numbers ----------
    # These are just quick summary stats using the whole dataset.
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Total Revenue", f"₹{df.revenue.sum():,.0f}")
    c2.metric("👥 Passengers", f"{df.passengers.sum():,}")
    c3.metric("🛣 Routes", df.route.nunique())
    c4.metric("🚌 Bus Types", df.bus_type.nunique())

    st.markdown("---")

    # ---------- Chart 1: Revenue by Route ----------
    st.subheader("📊 Revenue by Route")

    c1, c2 = st.columns([2, 1])
    with c1:
        revenue_bus = st.selectbox("Bus Type", ["All"] + buses, key="rev_bus")
    with c2:
        sort_option = st.selectbox(
            "Order", ["🎲 Random", "📈 Highest First", "📉 Lowest First"],
            key="sort_revenue"
        )

    # Filter by bus type if one was chosen
    filtered = df if revenue_bus == "All" else df[df.bus_type == revenue_bus]

    # Add up total revenue per route
    route_revenue = filtered.groupby("route", as_index=False).revenue.sum()

    # Sort the bars based on the dropdown choice
    if sort_option == "📉 Lowest First":
        route_revenue = route_revenue.sort_values("revenue", ascending=False)
    elif sort_option == "📈 Highest First":
        route_revenue = route_revenue.sort_values("revenue", ascending=True)
    else:
        route_revenue = route_revenue.sample(frac=1, random_state=42)

    fig = px.bar(
        route_revenue, x="revenue", y="route",
        orientation="h", color="revenue",
        color_continuous_scale="RdYlGn",
        text="revenue", title="Revenue Generated by Route"
    )
    fig.update_traces(texttemplate="₹%{x:,.0f}", textposition="inside")
    fig.update_layout(height=600, xaxis_title="Revenue (₹)", yaxis_title="Route")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ---------- Chart 2: Passengers by Bus Type ----------
    st.subheader("👥 Passenger Analysis")

    passenger_route = st.selectbox("Select Route", ["All"] + routes, key="pass_route")

    filtered = df if passenger_route == "All" else df[df.route == passenger_route]

    passenger_chart = filtered.groupby("bus_type", as_index=False).passengers.sum()

    fig2 = px.bar(
        passenger_chart, x="passengers", y="bus_type",
        orientation="h", color="passengers",
        color_continuous_scale="RdYlGn",
        text="passengers", title="Passengers by Bus Type"
    )
    fig2.update_traces(texttemplate="%{x:,.0f}", textposition="inside")
    fig2.update_layout(height=600, xaxis_title="Passengers", yaxis_title="Bus Type")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ---------- Chart 3: Bus Type Distribution (Pie) ----------
    st.subheader("🚌 Bus Type Distribution")

    pie_month = st.selectbox("Select Month", ["All"] + months, key="pie_month")

    filtered = df if pie_month == "All" else df[df.month == pie_month]

    bus_chart = filtered.groupby("bus_type", as_index=False).passengers.sum()

    fig3 = px.pie(
        bus_chart, names="bus_type", values="passengers",
        hole=.45, title="Passenger Distribution by Bus Type"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # ---------- Chart 4: Monthly Revenue Trend (Line) ----------
    st.subheader("📅 Monthly Revenue Trend")

    c1, c2 = st.columns(2)
    with c1:
        trend_route = st.selectbox("Route", ["All"] + routes, key="trend_route")
    with c2:
        trend_bus = st.selectbox("Bus Type", ["All"] + buses, key="trend_bus")

    filtered = df.copy()
    if trend_route != "All":
        filtered = filtered[filtered.route == trend_route]
    if trend_bus != "All":
        filtered = filtered[filtered.bus_type == trend_bus]

    monthly = filtered.groupby("month", as_index=False).revenue.sum()

    # Make sure months are ordered Jan -> Dec instead of alphabetically
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    monthly.month = pd.Categorical(monthly.month, categories=month_order, ordered=True)
    monthly = monthly.sort_values("month")

    fig4 = px.line(
        monthly, x="month", y="revenue",
        markers=True, title="Monthly Revenue Trend"
    )
    fig4.update_layout(height=500)
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # ---------- Table: Top 5 Revenue Routes ----------
    st.subheader("🏆 Top 5 Revenue Routes")

    top_bus = st.selectbox("Select Bus Type", ["All"] + buses, key="top_bus")

    filtered = df if top_bus == "All" else df[df.bus_type == top_bus]

    top = filtered.groupby("route", as_index=False).revenue.sum()
    top = top.sort_values("revenue", ascending=False).head(5)

    st.dataframe(top, use_container_width=True, hide_index=True)

# PAGE 3: ABOUT PROJECT
# Just static text describing the project, tools, and goals.
else:

    st.title("About Project")

    st.markdown("""
### 🚌 Smart Public Transport Performance & Passenger Trend Analysis

This project uses APSRTC transport data to study how buses and routes are performing. It was built using Python, 
Pandas for data handling, Plotly for charts, and Streamlit for the web dashboard. The main goals are to analyze revenue,
study passenger demand, compare routes and bus types, and track monthly trends. This kind of analysis can help transport authorities plan routes better,
allocate buses more efficiently, and make data-driven decisions. The dataset used is the APSRTC Transport Dataset from Kaggle,
 and the dashboard turns this raw data into easy-to-understand visual insights.
### 🛠 Technologies Used

- **Python** - Main programming language
- **Pandas** - Data cleaning and analysis
- **Plotly** - Interactive charts
- **Streamlit** - Web dashboard

### 🎯 Main Objectives

- Analyze total revenue
- Study passenger demand
- Compare route performance
- Compare different bus types
- Track monthly revenue
- Identify high and low performing routes
- Provide simple operational recommendations

### 💡 Why This Project Is Useful

Transport authorities can use this type of analysis to understand where demand is high, which routes generate more revenue and where bus allocation may need improvement.

### 📈 Key Benefits

- Better route planning
- Better bus allocation
- Revenue monitoring
- Passenger demand analysis
- Identification of performance patterns
- Data-driven decision making

### 📂 Dataset

**APSRTC Transport Dataset**

https://www.kaggle.com/datasets/balasrivatsa/apsrtc-public-transportation-data

The dashboard converts the raw dataset into interactive visual insights that are easier to understand and use.
""")