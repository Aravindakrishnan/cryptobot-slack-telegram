import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from utils.snapshot import snapshot_chart
from base64 import b64encode

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
        url = f"https://free.currconv.com/api/v7/convert?q={query}&compact={os.environ['CONVERT_API_KEY']}"
        fiat_price = requests.get(url).json()[query]
        return float(usd_price) * fiat_price

    def take_snapshot(self,coinname,chart_time):
        try:
            snapshot_chart(coinname,chart_time)    
            return self.host_snapshot("./static/charts/chart.png")
        except Exception as e:
            return e
    
    def host_snapshot(self,image_path):
        imgbb_url = 'https://api.imgbb.com/1/upload'
        response = requests.post(imgbb_url, 
        data = {
            'key': os.environ["IMGBB_API_KEY"], 
            'image':b64encode(open(image_path, 'rb').read()),
            'name': 'chart.png',
        }
        )
        return response.json()

