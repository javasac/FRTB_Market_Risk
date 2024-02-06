import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy.optimize import minimize

# stocks
tickers = ['NFLX', 'META', 'MSFT', 'GOOGL', 'AMZN']

end_date = datetime.today()
start_date = end_date - timedelta(days = 10 * 365)
RFR = .035

print (start_date)
print (end_date)

adj_close_df = pd.DataFrame()

for ticker in tickers:
    data = yf.download(ticker, start = start_date, end = end_date)
    adj_close_df[ticker] = data['Close']

print (adj_close_df)

log_returns = np.log (adj_close_df / adj_close_df.shift(1))
log_returns = log_returns.dropna()

cov_matrix = log_returns.cov() * 252

print(cov_matrix)

# calculate the standard deviation
def standard_deviation (weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)

# expected returns are based on historical returns
def expected_return (weights, log_returns):
    return np.sum(log_returns.mean() * weights) * 252

def sharpe_ratio (weights, log_returns, cov_matrix, RFR):
    return (expected_return (weights, log_returns) - RFR / standard_deviation (weights, cov_matrix))

def neg_sharpe_ratio (weights, log_returns, cov_matrix, RFR):
    return -sharpe_ratio(weights, log_returns, cov_matrix, RFR)

constraints = ({'type' : 'eq' , 'fun' : lambda weights : np.sum(weights) - 1})
bounds = [(0, 0.5) for _ in range (len(tickers))]

print (1/len(tickers))
print(len(tickers))

initial_weights = np.array([1/len(tickers)] * len(tickers))
print (initial_weights)

# set the initial weights
optimized_results = minimize(neg_sharpe_ratio, initial_weights, args=(log_returns, cov_matrix, RFR), method='SLSQP', constraints=constraints, bounds=bounds)
optimal_weights = optimized_results.x

for ticker, weight in zip(tickers, initial_weights):
  print(f"{ticker}: {weight:.4f}")

op_return = expected_return(optimal_weights, log_returns)
op_volat  = standard_deviation(initial_weights, cov_matrix)
op_ratio  = sharpe_ratio (initial_weights, log_returns, cov_matrix, RFR)

print(f"Expected Annual Return  : {op_return:.4f}")
print(f"Expected Volatility     : {op_volat:.4f}")
print(f"Expected Sharpe Ratio  : {op_ratio:.4f}")

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(tickers, optimal_weights)

plt.xlabel('Assets')
plt.ylabel('Optimal Weights')
plt.title('Optimal Portfolio Weights')

plt.show()

