import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

df = pd.read_csv("C:/Python/TSLA.csv")

print (df)

# create SMA
def SMA(data, period=30, column = 'Close'):
    return data[column].rolling(window=period).mean()

# create EMA
def EMA(data, period=30, column = 'Close'):
    return data[column].ewm(span=period, adjust=False).mean()

# create MACD
def MACD(data, period_long=26, period_short=12, period_signal=9, column='Close'):
    ShortEMA = EMA(data, period_short, column = column)
    LongEMA = EMA(data, period_short, column=column)
    data['MACD'] = ShortEMA - LongEMA
    data['Signal_Line'] = EMA(data, period_signal, column = 'MACD')
    return data

# create RSI
def RSI(data, period = 14, column='Close'):
    delta = data[column].diff(1)
    delta = delta[1:]
    up = delta.copy()
    down = delta.copy()
    up[up <0] = 0
    down[down > 0] = 0
    data['up'] = up
    data['down'] = down
    AVG_Gain = SMA(data, period, column = 'up')
    AVG_Loss = abs(SMA(data, period, column = 'down'))
    RS = AVG_Gain / AVG_Loss
    RSI = 100 - (100/(1 + RS))
    data['RSI'] = RSI
    return data

MACD(df)
RSI(df)
df['SMA'] = SMA(df)
df['EMA'] = EMA(df)

print(df)

column_list = ['EMA', 'SMA']

df[column_list].plot(figsize=(12.2, 6.4))
plt.title('EMA & SMA for Tesla')
plt.ylabel('USD Price')
plt.xlabel('Date')
plt.show()