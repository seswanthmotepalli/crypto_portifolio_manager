import pandas as pd
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "crypto_prices.csv"

# Load data
df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['coin', 'date'])

# Function to run stress scenario
def run_stress_test(drop_percent):
    stressed_df = df.copy()
    
    # Apply price shock
    stressed_df['stressed_price'] = stressed_df['price'] * (1 - drop_percent / 100)
    
    # Recalculate returns
    stressed_df['stressed_return'] = (
        stressed_df.groupby('coin')['stressed_price']
        .pct_change() * 100
    )
    
    # Calculate risk
    risk = stressed_df.groupby('coin')['stressed_return'].std()
    
    return risk

# Stress scenarios
scenarios = {
    "MILD (5%)": 5,
    "MODERATE (15%)": 15,
    "SEVERE (30%)": 30
}

print("STRESS TEST RESULTS\n")

for name, drop in scenarios.items():
    print(f"--- {name} CRASH ---")
    risk = run_stress_test(drop)
    print(risk)
    print()
