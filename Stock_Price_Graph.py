import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
def get_closing_prices(symbol, period):  # default value of 1 day.
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period)
        return data["Close"]
    except Exception as e:
        print("Failed to get required data.", e)

ticker = "SOXL"
period = "60mo"
prices_data = get_closing_prices(ticker, period)
prices_list = [round(val, 2) for val in prices_data.tolist()]  # Round the values
print(f"Latest month closing prices for {ticker} are: {prices_list}")

sns.lineplot(data=prices_data)
sns.set_theme()  # Default seaborn style
plt.xticks(rotation=30)
plt.title(f"Closing Stock Prices for {ticker}")
plt.show()