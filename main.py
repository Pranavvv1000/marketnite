import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the stock symbol and start and end dates
stock_symbol = 'TATAMOTORS.NS'
start_date = '2020-01-01'
end_date = '2023-03-31'

# Retrieve historical data for the stock
stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

# Calculate moving averages for 50 and 200 days
stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()

# Calculate the Relative Strength Index (RSI) and the Moving Average Convergence Divergence (MACD)
def calculate_technical_indicators(data):
    delta = data['Close'].diff()
    delta = delta[1:]

    up = delta.copy()
    up[up < 0] = 0

    down = delta.copy()
    down[down > 0] = 0

    AVG_Gain = up.rolling(window=14).mean()
    AVG_Loss = abs(down.rolling(window=14).mean())

    RS = AVG_Gain/AVG_Loss
    RSI = 100.0 - (100.0 / (1.0 + RS))

    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()

    MACD = exp1 - exp2
    signal = MACD.ewm(span=9, adjust=False).mean()

    return RSI, MACD, signal

RSI, MACD, signal = calculate_technical_indicators(stock_data)

# Plot the closing price, moving averages, RSI, and MACD
fig, axs = plt.subplots(3, sharex=True, figsize=(15,15))
axs[0].plot(stock_data['Close'])
axs[0].plot(stock_data['MA50'])
axs[0].plot(stock_data['MA200'])
axs[0].set_title('Stock Price')
axs[1].plot(RSI)
axs[1].set_title('Relative Strength Index (RSI)')
axs[2].plot(MACD)
axs[2].plot(signal)
axs[2].set_title('Moving Average Convergence Divergence (MACD)')

plt.show()

# Output conclusion
if stock_data['Close'][-1] > stock_data['MA50'][-1] and stock_data['MA50'][-1] > stock_data['MA200'][-1]:
    print(f"Tatamotors is currently in an uptrend.")
elif stock_data['Close'][-1] < stock_data['MA50'][-1] and stock_data['MA50'][-1] < stock_data['MA200'][-1]:
    print(f"Tatamotors is currently in a downtrend.")
else:
    print(f"Tatamotors is currently in a sideways trend.")