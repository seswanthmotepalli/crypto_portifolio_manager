import streamlit as st
import pandas as pd

from database.db import create_table, insert_data, fetch_data
from modules.fetch_data import get_historical_data
from modules.risk_analysis import analyze_risk
from modules.predictor import predict_future_price
from modules.portfolio import allocate
from modules.report import generate_report
from modules.graphs import (
    plot_prices,
    plot_allocation,
    plot_price_distribution,
    plot_volatility
)
from modules.alert import check_alerts

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Crypto Investment Manager", layout="wide")

# =========================
# CLEAN UI
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
.stButton>button {
    background-color: #1f6feb;
    color: white;
    border-radius: 8px;
    padding: 10px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #388bfd;
}
.card {
    background-color: #161b22;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    margin: 10px;
}
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
st.caption("Smart portfolio with risk analysis & ML prediction")

# =========================
# FETCH DATA
# =========================
if st.button("📥 Fetch 30 Days Data"):
    df = get_historical_data(30)
    insert_data(df)
    st.success("Data updated!")

# =========================
# LOAD DATA
# =========================
data = fetch_data()

if data:
    df = pd.DataFrame(data, columns=["date", "coin", "price"])
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date")

    # =========================
    # GRAPH + RISK
    # =========================
    left, right = st.columns([2, 1])

    with left:
        st.subheader("📈 Market Trends")
        st.pyplot(plot_prices(df))

    with right:
        st.subheader("⚠ Risk Overview")
        risk = analyze_risk(df)

        for coin in risk:
            level = risk[coin]["level"]

            if level == "HIGH":
                st.error(f"{coin.upper()} → HIGH")
            elif level == "MEDIUM":
                st.warning(f"{coin.upper()} → MEDIUM")
            else:
                st.success(f"{coin.upper()} → LOW")

    # =========================
    # 🔮 PREDICTION (CARD UI)
    # =========================
    st.subheader("🔮 Future Price Prediction")

    future_prices = {}
    for coin in df["coin"].unique():
        prices = df[df["coin"] == coin]["price"].values
        future_prices[coin] = predict_future_price(prices)

    cols = st.columns(len(future_prices))

    for i, coin in enumerate(future_prices):
        cols[i].markdown(
            f"<div class='card'><b>{coin.upper()}</b><br>${future_prices[coin]}</div>",
            unsafe_allow_html=True
        )

    # =========================
    # 💰 PORTFOLIO
    # =========================
    st.subheader("💰 Portfolio Allocation")

    allocation = allocate(risk, future_prices)

    cols = st.columns(len(allocation))

    for i, coin in enumerate(allocation):
        cols[i].markdown(
            f"<div class='card'><b>{coin.upper()}</b><br>{allocation[coin]}%</div>",
            unsafe_allow_html=True
        )

    # =========================
    # 📊 REPORT
    # =========================
    st.subheader("📊 Detailed Report")
    report = generate_report(risk, future_prices, allocation)
    st.dataframe(report, width="stretch")

    # =========================
    # 📊 EDA (FIXED)
    # =========================
    st.subheader("📊 Analysis")

    # Row 1
    colA, colB = st.columns(2)

    with colA:
        fig1 = plot_allocation(allocation)
        st.pyplot(fig1)

    with colB:
        fig2 = plot_volatility(risk)
        st.pyplot(fig2)

    # Row 2
    colC, colD = st.columns(2)

    with colC:
        fig3 = plot_price_distribution(df)
        st.pyplot(fig3)

    with colD:
        st.empty()

    # =========================
    # ALERTS
    # =========================
    st.subheader("🚨 Alerts")

    alerts = check_alerts(df)

    if alerts:
        for alert in alerts:
            st.error(alert)
    else:
        st.success("No major alerts")

else:
    st.warning("No data found. Click 'Fetch Data' first.")