from flask import Flask, jsonify , Response,render_template
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import io

app = Flask(__name__)

# Define the stock symbol and start and end dates
stock_symbol_rel = 'RELIANCE.NS'
stock_symbol_tata = 'TATAMOTORS.NS'
stock_symbol_icici = 'ICICIBANK.NS'
stock_symbol_hdfc = 'HDFCBANK.NS'
stock_symbol_axis = 'AXISBANK.NS'
start_date = '2022-01-01'
end_date = '2023-04-25'

# Retrieve historical data for the stock
stock_data_rel = yf.download(stock_symbol_rel, start=start_date, end=end_date)
stock_data_tata = yf.download(stock_symbol_tata, start=start_date, end=end_date)
stock_data_icici = yf.download(stock_symbol_icici, start=start_date, end=end_date)
stock_data_hdfc = yf.download(stock_symbol_hdfc, start=start_date, end=end_date)
stock_data_axis = yf.download(stock_symbol_axis, start=start_date, end=end_date)

# Calculate moving averages for 50 and 200 days
stock_data_rel['MA50'] = stock_data_rel['Close'].rolling(window=50).mean()
stock_data_rel['MA200'] = stock_data_rel['Close'].rolling(window=200).mean()
# Calculate moving averages for 50 and 200 days
stock_data_tata['MA50'] = stock_data_tata['Close'].rolling(window=50).mean()
stock_data_tata['MA200'] = stock_data_tata['Close'].rolling(window=200).mean()
# Calculate moving averages for 50 and 200 days
stock_data_icici['MA50'] = stock_data_icici['Close'].rolling(window=50).mean()
stock_data_icici['MA200'] = stock_data_icici['Close'].rolling(window=200).mean()
# Calculate moving averages for 50 and 200 days
stock_data_hdfc['MA50'] = stock_data_hdfc['Close'].rolling(window=50).mean()
stock_data_hdfc['MA200'] = stock_data_hdfc['Close'].rolling(window=200).mean()
# Calculate moving averages for 50 and 200 days
stock_data_axis['MA50'] = stock_data_axis['Close'].rolling(window=50).mean()
stock_data_axis['MA200'] = stock_data_axis['Close'].rolling(window=200).mean()

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


RSI, MACD, signal = calculate_technical_indicators(stock_data_rel)
RSI, MACD, signal = calculate_technical_indicators(stock_data_tata)
RSI, MACD, signal = calculate_technical_indicators(stock_data_icici)
RSI, MACD, signal = calculate_technical_indicators(stock_data_hdfc)
RSI, MACD, signal = calculate_technical_indicators(stock_data_axis)





@app.route('/reliance')
def reliance():
    
    output = ""
    if stock_data_rel['Close'][-1] > stock_data_rel['MA50'][-1] and stock_data_rel['MA50'][-1] > stock_data_rel['MA200'][-1]:
        output += f"RELIANCE is currently in an uptrend or in bullish Market, We suggest to Buy this stock now for short Range \n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."

    elif stock_data_rel['Close'][-1] < stock_data_rel['MA50'][-1] and stock_data_rel['MA50'][-1] < stock_data_rel['MA200'][-1]:
        output += f"RELIANCE is currently in a downtrend or in Bearish Market You can Buy at lowest price.\n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."
    else:
        output += f"RELIANCE is currently in a sideways trend.we suggest to hold the stocks.\n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."
    return output

@app.route('/relplot_png.png')
def relplot_png():
    
    # Create plot
    fig, axs = plt.subplots(3, sharex=True, figsize=(15, 15))
    axs[0].plot(stock_data_rel['Close'])
    axs[0].plot(stock_data_rel['MA50'])
    axs[0].plot(stock_data_rel['MA200'])
    axs[0].set_title('Stock Price')
    axs[1].plot(RSI)
    axs[1].set_title('Relative Strength Index (RSI)')
    axs[2].plot(MACD)
    axs[2].plot(signal)
    axs[2].set_title('Moving Average Convergence Divergence (MACD)')

    # Save plot to PNG image
    output_rel = io.BytesIO()
    FigureCanvas(fig).print_png(output_rel)
    return Response(output_rel.getvalue(), mimetype='image/png')


@app.route('/tatamotors')
def tatamotors():
    
    
    output = ""
    if stock_data_tata['Close'][-1] > stock_data_tata['MA50'][-1] and stock_data_tata['MA50'][-1] > stock_data_tata['MA200'][-1]:
        output += f"Tatamotors is currently in an uptrend or in bullish Market, We suggest to Buy this stock now for short Range \n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."

    elif stock_data_tata['Close'][-1] < stock_data_tata['MA50'][-1] and stock_data_tata['MA50'][-1] < stock_data_tata['MA200'][-1]:
        output += f"Tatamotors is currently in a downtrend or in Bearish Market You can Buy at lowest price.\n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."
    else:
        output += f"Tatamotors is currently in a sideways trend.we suggest to hold the stocks.\n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."
    return output

@app.route('/tataplot_png.png')
def tataplot_png():
    
    # Create plot
    fig, axs = plt.subplots(3, sharex=True, figsize=(15, 15))
    axs[0].plot(stock_data_tata['Close'])
    axs[0].plot(stock_data_tata['MA50'])
    axs[0].plot(stock_data_tata['MA200'])
    axs[0].set_title('Stock Price')
    axs[1].plot(RSI)
    axs[1].set_title('Relative Strength Index (RSI)')
    axs[2].plot(MACD)
    axs[2].plot(signal)
    axs[2].set_title('Moving Average Convergence Divergence (MACD)')

    # Save plot to PNG image
    output_tata = io.BytesIO()
    FigureCanvas(fig).print_png(output_tata)
    return Response(output_tata.getvalue(), mimetype='image/png')


@app.route('/ICICI')
def ICICI():
    
    
    output = ""
    if stock_data_icici['Close'][-1] > stock_data_icici['MA50'][-1] and stock_data_icici['MA50'][-1] > stock_data_icici['MA200'][-1]:
        output += f"ICICIBANK is currently in an uptrend or in bullish Market, We suggest to Buy this stock now for short Range \n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."

    elif stock_data_icici['Close'][-1] < stock_data_icici['MA50'][-1] and stock_data_icici['MA50'][-1] < stock_data_icici['MA200'][-1]:
        output += f"ICICIBANK is currently in a downtrend or in Bearish Market You can Buy at lowest price.\n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."
    else:
        output += f"ICICIBANK is currently in a sideways trend.we suggest to hold the stocks.\n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."
    return output

@app.route('/iciciplot_png.png')
def iciciplot_png():
    

    # Create plot
    fig, axs = plt.subplots(3, sharex=True, figsize=(15, 15))
    axs[0].plot(stock_data_icici['Close'])
    axs[0].plot(stock_data_icici['MA50'])
    axs[0].plot(stock_data_icici['MA200'])
    axs[0].set_title('Stock Price')
    axs[1].plot(RSI)
    axs[1].set_title('Relative Strength Index (RSI)')
    axs[2].plot(MACD)
    axs[2].plot(signal)
    axs[2].set_title('Moving Average Convergence Divergence (MACD)')

    # Save plot to PNG image
    output_icici = io.BytesIO()
    FigureCanvas(fig).print_png(output_icici)
    return Response(output_icici.getvalue(), mimetype='image/png')


@app.route('/hdfcbank')
def hdfcbank():
    
    
    output = ""
    if stock_data_hdfc['Close'][-1] > stock_data_hdfc['MA50'][-1] and stock_data_hdfc['MA50'][-1] > stock_data_hdfc['MA200'][-1]:
        output += f"HDFCBANK is currently in an uptrend or in bullish Market, We suggest to Buy this stock now for short Range \n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."

    elif stock_data_hdfc['Close'][-1] < stock_data_hdfc['MA50'][-1] and stock_data_hdfc['MA50'][-1] < stock_data_hdfc['MA200'][-1]:
        output += f"HDFCBANK is currently in a downtrend or in Bearish Market You can Buy at lowest price.\n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."
    else:
        output += f"HDFCBANK is currently in a sideways trend.we suggest to hold the stocks.\n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."
    return output

@app.route('/hdfcplot_png.png')
def hdfcplot_png():
   

    # Create plot
    fig, axs = plt.subplots(3, sharex=True, figsize=(15, 15))
    axs[0].plot(stock_data_hdfc['Close'])
    axs[0].plot(stock_data_hdfc['MA50'])
    axs[0].plot(stock_data_hdfc['MA200'])
    axs[0].set_title('Stock Price')
    axs[1].plot(RSI)
    axs[1].set_title('Relative Strength Index (RSI)')
    axs[2].plot(MACD)
    axs[2].plot(signal)
    axs[2].set_title('Moving Average Convergence Divergence (MACD)')

    # Save plot to PNG image
    output_hdfc = io.BytesIO()
    FigureCanvas(fig).print_png(output_hdfc)
    return Response(output_hdfc.getvalue(), mimetype='image/png')



@app.route('/axisbank')
def axisbank():
    
    
    output = ""
    if stock_data_axis['Close'][-1] > stock_data_axis['MA50'][-1] and stock_data_axis['MA50'][-1] > stock_data_axis['MA200'][-1]:
        output += f"AXISBANK is currently in an uptrend or in bullish Market, We suggest to Buy this stock now for short Range \n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."

    elif stock_data_axis['Close'][-1] < stock_data_axis['MA50'][-1] and stock_data_axis['MA50'][-1] < stock_data_axis['MA200'][-1]:
        output += f"AXISBANK is currently in a downtrend or in Bearish Market You can Buy at lowest price.\n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."
    else:
        output += f"AXISBANK is currently in a sideways trend.we suggest to hold the stocks.\n"
        output += "Tip:This is only Suggestion,Invest on your own Risk."
    return output

@app.route('/axisplot_png.png')
def axisplot_png():


    # Create plot
    fig, axs = plt.subplots(3, sharex=True, figsize=(15, 15))
    axs[0].plot(stock_data_axis['Close'])
    axs[0].plot(stock_data_axis['MA50'])
    axs[0].plot(stock_data_axis['MA200'])
    axs[0].set_title('Stock Price')
    axs[1].plot(RSI)
    axs[1].set_title('Relative Strength Index (RSI)')
    axs[2].plot(MACD)
    axs[2].plot(signal)
    axs[2].set_title('Moving Average Convergence Divergence (MACD)')

    # Save plot to PNG image
    output_axis = io.BytesIO()
    FigureCanvas(fig).print_png(output_axis)
    return Response(output_axis.getvalue(), mimetype='image/png')




if __name__ == '__main__':
    app.run(debug=True)
