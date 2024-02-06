from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.greeks.analytical import delta, gamma, vega, theta, rho

# Option parameters
S = 100  # Current stock price
K = 105  # Option strike price
t = 0.5  # Time to expiration (in years)
r = 0.05  # Risk-free interest rate
sigma = 0.2  # Volatility

# Black-Scholes parameters
option_type = 'c'  # 'c' for call, 'p' for put

# Calculate option price and Greeks
option_price = black_scholes(option_type, S, K, t, r, sigma)
delta = delta (option_type, S, K, t, r, sigma)
gamma = gamma (option_type, S, K, t, r, sigma)
theta = theta (option_type, S, K, t, r, sigma)
vega = vega (option_type, S, K, t, r, sigma)
rho = rho (option_type, S, K, t, r, sigma)

# Display results
print(f"Option Price: {option_price:.4f}")
print(f"Option Delta: {delta:.4f}")
print(f"Option Gamma: {gamma:.4f}")
print(f"Option Theta: {theta:.4f}")
print(f"Option Vega: {vega:.4f}")
print(f"Option Rho: {rho:.4f}")

