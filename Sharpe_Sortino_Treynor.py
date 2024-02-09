import numpy as np

def calculate_sharpe_ratio(returns, risk_free_rate):
    sharpe_ratio = (np.mean(returns) - risk_free_rate) / np.std(returns)
    return sharpe_ratio

def calculate_sortino_ratio(returns, risk_free_rate, target_return=0):
    downside_returns = returns[returns < target_return]
    downside_deviation = np.std(downside_returns)
    sortino_ratio = (np.mean(returns) - risk_free_rate) / downside_deviation
    return sortino_ratio

def calculate_treynor_ratio(returns, market_returns, risk_free_rate):
    beta = np.cov(returns, market_returns)[0, 1] / np.var(market_returns)
    treynor_ratio = (np.mean(returns) - risk_free_rate) / beta
    return treynor_ratio

# Example usage
returns = np.random.randn(100)
risk_free_rate = 0.03
market_returns = np.random.randn(100)

sharpe_ratio = calculate_sharpe_ratio(returns, risk_free_rate)
sortino_ratio = calculate_sortino_ratio(returns, risk_free_rate)
treynor_ratio = calculate_treynor_ratio(returns, market_returns, risk_free_rate)

print("Sharpe Ratio:", sharpe_ratio)
print("Sortino Ratio:", sortino_ratio)
print("Treynor Ratio:", treynor_ratio)
