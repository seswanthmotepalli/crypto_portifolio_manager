import matplotlib.pyplot as plt

def plot_prices(df):
    fig, ax = plt.subplots()   # ✅ create clean figure

    coins = df["coin"].unique()

    for coin in coins:
        data = df[df["coin"] == coin]

        # ✅ use date on X-axis
        ax.plot(data["date"], data["price"], label=coin)

    ax.set_title("Price Trends")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()

    plt.xticks(rotation=45)   # ✅ rotate for readability
    plt.tight_layout()

    return fig   # ✅ return figure instead of plt