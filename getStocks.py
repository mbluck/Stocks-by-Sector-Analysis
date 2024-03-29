import yahoo_fin.stock_info as si
import yfinance as yf
import pandas as pd

tickers = si.tickers_nasdaq()

sectors, prices, volumes, fifty_day_averages = ([None]*len(tickers) for i in range(4))

for i, ticker in enumerate(tickers):
    ticker_obj = yf.Ticker(ticker)

    try:
        sector = ticker_obj.info['sector']
    except:
        sector = -1
    sectors[i] = sector

    try:
        price = ticker_obj.info['currentPrice']
    except:
        price = str(-1)
    prices[i] = price

    try:
        volume = ticker_obj.info['volume']
    except:
        volume = str(-1)
    volumes[i] = volume

    try:
        fifty_day_average = ticker_obj.info['fiftyDayAverage']
    except: fifty_day_average = str(-1)
    fifty_day_averages[i] = fifty_day_average
        
    
data_dict = {'Ticker': tickers,
             'Sector': sectors,
             'Price': prices,
             'Volume': volumes,
             'Fifty Day Average': fifty_day_averages}

data = pd.DataFrame(data_dict)
data.to_csv('data/stock_data.csv', index=False)
