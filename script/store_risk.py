import sqlite3
from pathlib import Path
import pandas as pd

# Load processed data (reuse logic or import function later)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "crypto_prices.csv"
DB_PATH = BASE_DIR / "db" / "crypto.db"

df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by=['coin', 'date'])
df['daily_return'] = df.groupby('coin')['price'].pct_change() * 100

# Calculate risk per coin
risk_df = df.groupby('coin')['daily_return'].std().reset_index()
risk_df.rename(columns={'daily_return': 'risk'}, inplace=True)

# Store in DB
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

for _, row in risk_df.iterrows():
    cur.execute(
        "INSERT INTO trends (coin, date, avg_return, risk) VALUES (?, ?, ?, ?)",
        (row['coin'], "SUMMARY", None, row['risk'])
    )

conn.commit()
conn.close()

print("RISK STORED IN DATABASE")
