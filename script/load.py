import pandas as pd
import os

# Get project root safely
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "crypto_prices.csv")

# Load data
df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])

# Sort for time-series correctness
df = df.sort_values(by=['coin', 'date'])