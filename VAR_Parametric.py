import numpy as np, pandas as pd, yfinance as yf, datetime as dt, matplotlib.pyplot as plt
from scipy.stats import norm

years = 10
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days = 365 * years)

tickers = ['JPM', 'AAPL', 'LLY', 'META', 'NVDA']
weights = np.array([1/len(tickers)] * len(tickers))
print(weights)

adj_close_df = pd.DataFrame()

# download the Adjusted close of all the Tickers
for tick in tickers:
    data = yf.download(tick, start = startDate, end = endDate)
    adj_close_df[tick] = data['Adj Close']

print(adj_close_df)

log_returns = np.log(adj_close_df / adj_close_df.shift(1))
log_returns = log_returns.dropna()

print(log_returns)

portfolio_value = 123456

# calc the historical returns of the Portfolio
historical_returns = (log_returns * weights).sum(axis=1)
print(historical_returns)

days = 10
historical_x_day_returns = historical_returns.rolling(window = days).sum()

# create a COVAR matric for all securities
cov_matrix = log_returns.cov() * 252
port_std_dev = np.sqrt(weights.T @ cov_matrix @ weights)

confidence_levels = [0.9, 0.95, 0.99]

VaRs = []

for cl in confidence_levels:
    VaR = portfolio_value * port_std_dev * norm.ppf(cl) * np.sqrt(days/252)
    VaRs.append(VaR)

print (VaRs)

print(f'{"Confidence Level":<20} {"Value at Risk" : <20}')
print('-' * 40)

# print each Confidence level and its corresponding VaR value
for cl, VaR in zip(confidence_levels, VaRs):
    print(f'{cl * 100 :> 6.0f}%:  {"":<8} ${VaR:>10.4f}')

historical_x_day_returns_dollar = historical_x_day_returns * portfolio_value

plt.hist(historical_x_day_returns_dollar, bins=50, density=True, alpha = 0.5, label=f'{days} - Day Returns')

for cl, VaR in zip(confidence_levels, VaRs):
    plt.axvline(x=-VaR, linestyle='--', color='r', label='VaR at {}% Confidence'.format(int(cl * 100)))

plt.xlabel(f'{days} - Day Portfolio Return ($)')
plt.ylabel('Frequency')
plt.title(f'Distribution of Portfolio {days} - Days returns and Parametric VaR estimates')
plt.legend()
plt.show()
