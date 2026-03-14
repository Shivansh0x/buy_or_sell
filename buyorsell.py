import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
ticker = "MSFT"
df = yf.download(ticker, start="2020-01-01", end="2025-01-01")

df["big"] = df["Close"].rolling(200).mean()
df["small"] = df["Close"].rolling(5).mean()
df.dropna()

df["signal"] = np.where(df["small"] > df["big"], 1, 0)

df["trades"] = df["signal"].diff()

buys = df[df["trades"] == 1]
sells = df[df["trades"] == -1]

print("Buy at: ")
print(buys.index)
print("Sell at:")
print(sells.index)

df["returns"] = df["Close"].pct_change()
df["buy_returns"] = (1+df["returns"]).cumprod()
df["profit_returns"] = (1 + df["returns"]*df["signal"]).cumprod()
capital = 1000
df["profit"] = (capital*df["profit_returns"]) - capital
df["buy_profit"] = (capital*df["buy_returns"]) - capital

plt.plot(df.index, df["Close"], linestyle="-", label="MSFT", zorder=1)
plt.scatter(buys.index, buys["Close"], marker="^", color="green", label="Buy Signal", zorder=2)
plt.scatter(sells.index, sells["Close"], marker="v", color="red", label="Sell Signal",zorder=2)
plt.plot(df.index, df["profit"], color="green", linestyle="--", zorder=1, label="Profit")
plt.plot(df.index, df["buy_profit"], color="purple", linestyle="--", zorder=1, label="Profit if bought from start")
plt.grid(alpha=0.1)
plt.legend()
plt.show()

