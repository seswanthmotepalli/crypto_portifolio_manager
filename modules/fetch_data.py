import requests
import pandas as pd
from datetime import datetime
from config import COINS
import time

def get_historical_data(days=30):
    all_data = []

    for coin in COINS:
        url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"

        params = {
            "vs_currency": "usd",
            "days": days
        }

        try:
            res = requests.get(url, params=params)

            if res.status_code != 200:
                print(f"Error fetching {coin}: {res.status_code}")
                continue

            data = res.json()

            if "prices" not in data:
                print(f"No data for {coin}: {data}")
                continue

            for price in data["prices"]:
                timestamp = datetime.fromtimestamp(price[0] / 1000)

                all_data.append({
                    "date": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "coin": coin,
                    "price": price[1]
                })

            time.sleep(1)  # avoid rate limit

        except Exception as e:
            print(f"Error fetching {coin}: {e}")

    return pd.DataFrame(all_data)