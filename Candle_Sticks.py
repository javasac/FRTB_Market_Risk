import yfinance as yf, pandas as pd, numpy as np, matplotlib.pyplot as plt, mplfinance as mpf
from datetime import datetime, timedelta
from scipy.optimize import minimize

end_date = datetime.today()
start_date = end_date - timedelta(days = 2 * 365)

data = yf.download('NVDA', start = start_date, end = end_date)

colors = mpf.make_marketcolors(up="#00ff00", down="#ff0000", wick="inherit", edge="inherit", volume="in")

mpf.plot(data, type="candle", style="yahoo", volume=True)


