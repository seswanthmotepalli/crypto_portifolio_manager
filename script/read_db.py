import sqlite3
import pandas as pd

conn = sqlite3.connect("db/crypto.db")

df = pd.read_sql("SELECT * FROM trends", conn)

conn.close()

print(df)
