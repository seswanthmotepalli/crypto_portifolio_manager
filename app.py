import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database.db import create_table, insert_data, fetch_data
from modules.fetch_data import get_historical_data
from modules.risk_analysis import analyze_risk
from modules.predictor import predict_trend
from modules.portfolio import allocate
from modules.rules import apply_rules
from modules.report import generate_report
from modules.graphs import plot_prices
from modules.alert import check_alerts

# =========================
# PAGE CONFIG (Professional UI)
# =========================
st.set_page_config(
    page_title="Crypto Investment Manager",
    layout="wide"
)

# =========================
# CUSTOM CSS (Dark Theme + Styling)
# =========================
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.stApp {
    background-color: #0e1117;
    color: white;
}
.card {
    padding: 15px;
    border-radius: 10px;
    background-color: #1c1f26;
    margin-bottom: 10px;
}
.green {color: #00ff9c;}
.red {color: #ff4b4b;}
.yellow {color: #ffd700;}
</style>
""", unsafe_allow_html=True)

# =========================
# INIT DB
# =========================
create_table()

# =========================
# HEADER
# =========================
st.title("🚀 Crypto Investment Manager")
st.markdown("Smart portfolio analysis with risk-based allocation")

# =========================
# BUTTON ROW
# =========================
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Fetch 30 Days Data"):
        df = get_historical_data(30)
        insert_data(df)
        st.success("Data updated!")

with col2:
    if st.button("🧹 Clear Database"):
        st.warning("Delete data/prices.db manually for clean reset")

# =========================
# LOAD DATA
# =========================
data = fetch_data()

if data:
    df = pd.DataFrame(data, columns=["date", "coin", "price"])
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date")

    # =========================
    # TOP SECTION (2 columns)
    # =========================
    left, right = st.columns([2, 1])

    # =========================
    # 📊 GRAPH
    # =========================
    with left:
        st.subheader("📈 Market Trends")
        fig = plot_prices(df)
        st.pyplot(fig)

    # =========================
    # ⚠ RISK PANEL
    # =========================
    with right:
        st.subheader("⚠ Risk Overview")

        risk = analyze_risk(df)

        for coin in risk:
            level = risk[coin]["level"]
            value = round(risk[coin]["value"], 5)

            if level == "HIGH":
                st.markdown(f"<div class='card red'><b>{coin.upper()}</b><br>HIGH RISK<br>{value}</div>", unsafe_allow_html=True)
            elif level == "MEDIUM":
                st.markdown(f"<div class='card yellow'><b>{coin.upper()}</b><br>MEDIUM RISK<br>{value}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='card green'><b>{coin.upper()}</b><br>LOW RISK<br>{value}</div>", unsafe_allow_html=True)

    # =========================
    # TREND + PORTFOLIO
    # =========================
    trend = {}
    for coin in df["coin"].unique():
        prices = df[df["coin"] == coin]["price"].values
        trend[coin] = predict_trend(prices)

    allocation = allocate(risk, trend)
    allocation = apply_rules(allocation)

    st.subheader("💰 Portfolio Allocation")

    colA, colB, colC = st.columns(3)

    i = 0
    for coin in allocation:
        value = allocation[coin]

        if i % 3 == 0:
            col = colA
        elif i % 3 == 1:
            col = colB
        else:
            col = colC

        col.markdown(f"<div class='card'><b>{coin.upper()}</b><br>{value}%</div>", unsafe_allow_html=True)
        i += 1

    # =========================
    # REPORT TABLE
    # =========================
    report = generate_report(risk, trend, allocation)

    st.subheader("📄 Detailed Report")
    st.dataframe(report, use_container_width=True)

    # =========================
    # ALERTS
    # =========================
    alerts = check_alerts(df)

    st.subheader("🚨 Alerts")

    if alerts:
        for alert in alerts:
            st.error(alert)
    else:
        st.success("No major market alerts")

else:
    st.warning("⚠ No data found. Fetch data first.")