import sqlite3
import pandas as pd
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "crypto.db"
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

REPORT_PATH = REPORT_DIR / "risk_report.csv"

# Read data from DB
conn = sqlite3.connect(DB_PATH)

df = pd.read_sql("""
SELECT coin, risk
FROM trends
WHERE date = 'PARALLEL'
""", conn)

conn.close()

# Clean duplicates if any
df = df.groupby("coin", as_index=False)["risk"].mean()

# Save to CSV
df.to_csv(REPORT_PATH, index=False)

print("RISK REPORT GENERATED")
print(f"Saved at: {REPORT_PATH}")
print("\nREPORT PREVIEW:")
print(df)
