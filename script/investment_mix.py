import sqlite3
from pathlib import Path
import pandas as pd

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "crypto.db"

# Load risk data from DB
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT coin, risk FROM trends WHERE date='PARALLEL'", conn)
conn.close()

print("RISK DATA:")
print(df)

# Remove duplicates (if script ran multiple times)
df = df.groupby("coin", as_index=False)["risk"].mean()

# Rule 1: Inverse risk (lower risk → higher weight)
df["inv_risk"] = 1 / df["risk"]

# Rule 2: Normalize to 100%
df["allocation_pct"] = (df["inv_risk"] / df["inv_risk"].sum()) * 100

# Rule 3: Cap max allocation (risk control)
MAX_ALLOC = 50  # no coin gets more than 50%

df["allocation_pct"] = df["allocation_pct"].clip(upper=MAX_ALLOC)

# Re-normalize after cap
df["allocation_pct"] = (df["allocation_pct"] / df["allocation_pct"].sum()) * 100

print("\nRECOMMENDED INVESTMENT MIX:")
print(df[["coin", "allocation_pct"]])
