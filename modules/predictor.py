import numpy as np

def predict_trend(prices):
    if len(prices) < 3:
        return 0

    x = np.arange(len(prices))
    y = prices

    slope = np.polyfit(x, y, 1)[0]
    return slope