import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from base64 import b64encode
import utils.candle as candle 

ENV_PATH= Path(".") / "../.env"
load_dotenv(dotenv_path=ENV_PATH)

class Crypto:

    def __init__(self):
        url = "https://api.coinlore.net/api/tickers/?start=0&limit=100"
        self.coins = requests.get(url).json()
    
    def get_coins(self):
        return self.coins

    def get_coin(self,coin_name):
        for coin in self.coins["data"]:
            if coin["nameid"] == coin_name.lower() or coin["symbol"].lower() == coin_name.lower():
                return coin
        return {}
        
    def convert_currency(self,usd_price,fiat_name):
        query = f"USD_{fiat_name.upper()}"
        url = f"https://free.currconv.com/api/v7/convert?q={query}&compact=ultra&apiKey={os.environ['CONVERT_API_KEY']}"
        fiat_price = requests.get(url).json()[query]
        return float(usd_price) * fiat_price

    def get_candles(self,coinname,chart_interval):
        try:
            symbol = coinname.upper()
            candle.save_chart(symbol=symbol,interval=chart_interval)
            return self.host_snapshot("chart.png")
        except Exception as e:
            return e
    
    def host_snapshot(self,path):
        imgbb_url = 'https://api.imgbb.com/1/upload'
        abs_path = os.path.abspath(path)
        response = requests.post(imgbb_url, 
        data = {
            'key': os.environ["IMGBB_API_KEY"], 
            'image':b64encode(open(abs_path, 'rb').read()),
            'name': 'chart.png',
        }
        )
        return response.json()

    