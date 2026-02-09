import sqlite3
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Paths (safe & professional)
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "crypto.db"
DATA_PATH = BASE_DIR / "data" / "crypto_prices.csv"

# Load price data
df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['coin', 'date'])
df['daily_return'] = df.groupby('coin')['price'].pct_change() * 100

# Function to calculate risk for ONE coin
def risk_for_coin(coin):
    coin_df = df[df['coin'] == coin]
    risk = coin_df['daily_return'].std()
    return coin, risk

# Coins list
coins = df['coin'].unique()

# Run risk checks in parallel
with ThreadPoolExecutor() as executor:
    results = executor.map(risk_for_coin, coins)

# Store results in DB
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

for coin, risk in results:
    cur.execute(
        "INSERT INTO trends (coin, date, avg_return, risk) VALUES (?, ?, ?, ?)",
        (coin, "PARALLEL", None, risk)
    )
    print(f"{coin} risk calculated & stored")

conn.commit()
conn.close()

print("\nPARALLEL RISK CHECK COMPLETE")
