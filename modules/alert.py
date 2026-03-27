def check_alerts(df, threshold=5):
    alerts = []

    for coin in df["coin"].unique():
        prices = df[df["coin"] == coin]["price"].values

        if len(prices) > 1:
            change = ((prices[-1] - prices[-2]) / prices[-2]) * 100

            if abs(change) > threshold:
                alerts.append(f"{coin} moved {round(change,2)}%")

    return alerts