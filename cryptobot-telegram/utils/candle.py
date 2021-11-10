import requests
import pandas as pd
import mplfinance as mpf
from datetime import datetime , date

def save_chart(symbol,interval="1d"):
    """
        save_chart() method saves the candlechart image for the specified coin 
        and also returns the dataframe for the specified coin.
    """

    if(interval not in "1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M"):
        raise Exception("Invalid interval !")

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
    
    current_time = datetime.now().time()
    current_date = date.today().strftime("%d/%m/%Y")
    title = f"{symbol}|{current_date}|{current_time}"

    try:
        dataframe = pd.DataFrame(raw_data).set_index("Date")
        mpf.plot(dataframe,type="candle",style="yahoo",title=title,ylabel="Price in USDT",savefig="chart.png")    
        return dataframe
    except Exception as e:
        print(e)