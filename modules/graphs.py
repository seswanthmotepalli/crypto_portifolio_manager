import matplotlib.pyplot as plt

def plot_prices(df):
    fig, ax = plt.subplots(figsize=(6,3))

    for coin in df["coin"].unique():
        data = df[df["coin"] == coin]
        ax.plot(data["date"], data["price"], label=coin)

    ax.legend()
    ax.set_title("Price Trends")
    plt.xticks(rotation=45)
    return fig


def plot_allocation(allocation):
    fig, ax = plt.subplots(figsize=(4,4))
    ax.pie(allocation.values(), labels=allocation.keys(), autopct="%1.1f%%")
    ax.set_title("Portfolio Allocation")
    return fig


def plot_price_distribution(df):
    fig, ax = plt.subplots(figsize=(5,3))

    for coin in df["coin"].unique():
        ax.hist(df[df["coin"] == coin]["price"], alpha=0.5, label=coin)

    ax.legend()
    ax.set_title("Price Distribution")
    return fig


def plot_volatility(risk):
    fig, ax = plt.subplots(figsize=(5,3))

    coins = list(risk.keys())
    values = [risk[c]["value"] for c in coins]

    ax.bar(coins, values)
    ax.set_title("Volatility")
    return fig