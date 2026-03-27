import sqlite3

DB_FILE = "data/prices.db"

def create_table():
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS prices(
        date TEXT,
        coin TEXT,
        price REAL
    )
    """)

    conn.commit()
    conn.close()


def insert_data(df):
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("prices", conn, if_exists="append", index=False)
    conn.close()


def fetch_data():
    conn = sqlite3.connect(DB_FILE)
    data = conn.execute("SELECT * FROM prices").fetchall()
    conn.close()
    return data