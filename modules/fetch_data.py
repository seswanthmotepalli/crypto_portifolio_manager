import requests
import pandas as pd
from datetime import datetime
from config import COINS

def get_historical_data(days=30):
    all_data = []

    for coin in COINS:
        url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days
        }

        res = requests.get(url, params=params)
        data = res.json()

        for price in data["prices"]:
            timestamp = datetime.fromtimestamp(price[0] / 1000)

            all_data.append({
                "date": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "coin": coin,
                "price": price[1]
            })

    return pd.DataFrame(all_data)