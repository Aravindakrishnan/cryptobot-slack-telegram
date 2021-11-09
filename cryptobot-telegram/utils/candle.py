import requests
import pandas as pd
import mplfinance as mpf

def save_chart(symbol,interval="1d"):
    url = f"https://api.binance.com/api/v1/klines?symbol={symbol}USDT&interval={interval}&limit=100"
    candles = requests.get(url).json()

    time_c = []
    open_c = []
    high_c = []
    low_c = []
    close_c = []
    
    for candle in candles:
        time_c.append(float(candle[0]))
        open_c.append(float(candle[1]))
        high_c.append(float(candle[2]))
        low_c.append(float(candle[3]))
        close_c.append(float(candle[4]))

    raw_data = {
        'Date' : pd.DatetimeIndex(time_c),
        'Open' : open_c,
        'High' : high_c,
        'Low' : low_c,
        'Close' : close_c
    }

    dataframe = pd.DataFrame(raw_data).set_index("Date")
    mpf.plot(dataframe,type="candle",style="yahoo",title=symbol,ylabel="Price in USDT",savefig="chart.png")    
    return dataframe
