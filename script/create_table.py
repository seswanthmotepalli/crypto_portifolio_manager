import sqlite3

conn = sqlite3.connect("db/crypto.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS trends (
    coin TEXT,
    date TEXT,
    avg_return REAL,
    risk REAL
)
""")

conn.commit()
conn.close()

print("TABLE 'trends' CREATED SUCCESSFULLY")
