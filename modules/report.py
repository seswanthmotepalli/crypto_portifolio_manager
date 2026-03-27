import pandas as pd

def generate_report(risk, trend, allocation):
    data = []

    for coin in risk:
        data.append({
            "Coin": coin,
            "Risk Value": round(risk[coin]["value"], 5),
            "Risk Level": risk[coin]["level"],
            "Trend": round(trend.get(coin, 0), 5),
            "Allocation %": allocation[coin]
        })

    df = pd.DataFrame(data)
    df.to_csv("reports/report.csv", index=False)
    return df