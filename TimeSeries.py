import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Load the time series data
data = pd.read_csv('your_time_series_data.csv')

# Convert 'date' column to datetime format and set it as index
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Visualize the time series data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data['value'], color='blue')
plt.title('Time Series Data')
plt.xlabel('Date')
plt.ylabel('Value')
plt.show()

# Perform time series decomposition (additive model)
decomposition = seasonal_decompose(data['value'], model='additive', period=12)

# Plot decomposition
plt.figure(figsize=(10, 8))

plt.subplot(4, 1, 1)
plt.plot(data.index, data['value'], label='Original', color='blue')
plt.legend(loc='upper left')

plt.subplot(4, 1, 2)
plt.plot(data.index, decomposition.trend, label='Trend', color='red')
plt.legend(loc='upper left')

plt.subplot(4, 1, 3)
plt.plot(data.index, decomposition.seasonal, label='Seasonal', color='green')
plt.legend(loc='upper left')

plt.subplot(4, 1, 4)
plt.plot(data.index, decomposition.resid, label='Residual', color='purple')
plt.legend(loc='upper left')

plt.tight_layout()
plt.show()
