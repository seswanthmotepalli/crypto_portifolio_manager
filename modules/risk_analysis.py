import numpy as np
from concurrent.futures import ThreadPoolExecutor

# ✅ Step 1: Calculate volatility safely
def volatility(prices):
    if len(prices) < 2:
        return 0

    returns = np.diff(prices) / prices[:-1]

    if len(returns) == 0:
        return 0

    return np.std(returns)


# ✅ Step 2: Classify risk
def classify_risk(vol):
    if vol < 0.01:
        return "LOW"
    elif vol < 0.03:
        return "MEDIUM"
    else:
        return "HIGH"


# ✅ Step 3: Worker function
def risk_worker(df, coin):
    prices = df[df["coin"] == coin]["price"].values
    vol = volatility(prices)
    level = classify_risk(vol)

    return coin, {
        "value": vol,
        "level": level
    }


# ✅ Step 4: Parallel execution
def analyze_risk(df):
    coins = df["coin"].unique()
    result = {}

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(risk_worker, df, c) for c in coins]

        for f in futures:
            coin, data = f.result()
            result[coin] = data

    return result