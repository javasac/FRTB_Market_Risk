import pandas as pd, yfinance as yf, numpy as np, datetime as dt, matplotlib.pyplot as plt
import plotly.express as px, seaborn as sns
from pypfopt import risk_models, expected_returns
from pypfopt.expected_returns import ema_historical_return
from pypfopt.risk_models import exp_cov
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.plotting import plot_efficient_frontier
from pypfopt.plotting import plot_weights
from pypfopt.cla import CLA

symbols = ['MSFT', 'AAPL', 'TSLA', 'NFLX', 'NVDA', 'CAT', 'XLE', 'JPM']

endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days = 365 * 5)

data = yf.download(symbols, start = startDate, end = endDate)
print(data.head())

portfolio_returns = data['Adj Close'].pct_change().dropna()

port_comps_rets_cumprod = portfolio_returns.add(1).cumprod().sub(1) * 100

fig = px.line(port_comps_rets_cumprod,
              x=port_comps_rets_cumprod.index,
              y=port_comps_rets_cumprod.columns,
              title='Cumulative Returns of Portfolio Stocks (2018-2023)'
            )

fig.update_xaxes(title_text = 'Date')
fig.update_yaxes(title_text = 'Cumulative return in X%')

fig.show()

#import S&P data for performance comparison
spy = yf.download('^GSPC', start = startDate, end = endDate)
print(spy.head())

# create a correlation heatmap to visualize portfolio asset neutrality
port_corr = port_comps_rets_cumprod.corr()
print(sns.heatmap(port_corr))

train = portfolio_returns[:"2021-05-30"]
test = portfolio_returns["2021-05-31":]

mu = expected_returns.ema_historical_return(train, returns_data=True, span = 500)
Sigma = risk_models.exp_cov(train, returns_data=True, span=180)

print(mu)

ret_ef = np.arange(0, 2.448605, .01)
vol_ef = []

for i in np.arange(0, 2.448605, .01):
    ef = EfficientFrontier(mu, Sigma)
    ef.efficient_return(i)
    vol_ef.append(ef.portfolio_performance()[1])

ef = EfficientFrontier(mu, Sigma)
ef.min_volatility()
min_vol_ret = ef.portfolio_performance()[0]
min_vol_vol = ef.portfolio_performance()[1]

ef = EfficientFrontier(mu, Sigma)
ef.max_sharpe(risk_free_rate=0.009)
max_sharpe_ret = ef.portfolio_performance()[0]
max_sharpe_vol = ef.portfolio_performance()[1]

sns.set()

fig, ax = plt.subplots(figsize = [15, 10])

sns.lineplot(x=vol_ef, y=ret_ef, label = "Efficient Frontier", ax=ax)

sns.scatterplot(x=[min_vol_vol], y=[min_vol_ret], ax=ax, label = "Minimum Variance Portfolio", color = "purple", s=100)

sns.scatterplot(x=[max_sharpe_vol], y=[max_sharpe_ret], ax=ax, label = "Maximum Sharpe Portfolio", color = "green", s=100)

#sns.lineplot(x = [0, max_sharpe_vol, 1], y = [0.009, max_sharpe_ret, 2.448605], label = "Capital Market Line", color = "r", s=100)

sns.lineplot(x=[0, max_sharpe_vol, 1], y=[0.009, max_sharpe_ret, 2.448605], ax=ax, label = "Capital Market Line", color = "r")

ax.set(xlim = [0, 0.4])
ax.set(ylim = [0, 1])
ax.set_xlabel("Volatility")
ax.set_ylabel("Mean Return")
plt.legend(fontsize = 'large')
plt.title("Efficient Frontier")
plt.show()
