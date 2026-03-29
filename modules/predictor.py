import numpy as np
from sklearn.linear_model import LinearRegression

def predict_future_price(prices, steps=1):
    if len(prices) < 3:
        return round(prices[-1], 2)

    X = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices)

    model = LinearRegression()
    model.fit(X, y)

    future_x = np.array([[len(prices) + steps]])
    future_price = model.predict(future_x)[0]

    return round(float(future_price), 2)