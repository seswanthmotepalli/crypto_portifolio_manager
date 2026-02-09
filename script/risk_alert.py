import sqlite3
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "crypto.db"

# Alert thresholds
HIGH_RISK = 0.05
CRITICAL_RISK = 0.08

# Read latest risk data
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
SELECT coin, risk
FROM trends
WHERE date = 'PARALLEL'
""")

rows = cur.fetchall()
conn.close()

print("RISK ALERT CHECK\n")

for coin, risk in rows:
    if risk is None:
        continue

    if risk >= CRITICAL_RISK:
        print(f"🚨 CRITICAL ALERT: {coin} risk is VERY HIGH ({risk:.4f})")
    elif risk >= HIGH_RISK:
        print(f"⚠️ HIGH RISK ALERT: {coin} risk is high ({risk:.4f})")
    else:
        print(f"✅ SAFE: {coin} risk is normal ({risk:.4f})")
