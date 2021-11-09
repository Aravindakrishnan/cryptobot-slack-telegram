# Crypto module used for getting JSON of cryptocurrencies 

import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from base64 import b64encode
import utils.candle as candle 

# Commented it for hosting in ec2 server 

# TODO: uncomment it and create a .env in /cryptobot-slack directory.
# Paste needed API_KEYS ref : README.md

# ENV_PATH= Path(".") / "../.env"
# load_dotenv(dotenv_path=ENV_PATH)

class Crypto:

    def __init__(self):
        url = "https://api.coinlore.net/api/tickers/?start=0&limit=100"
        self.coins = requests.get(url).json()
    
    def get_coins(self):
        """
            get_coin() method returns complete JSON of top 100 cryptocurrencies.
        """
        return self.coins

    def get_coin(self,coin_name):
        """
            get_coin() method return the JSON of specified coin
        """
        for coin in self.coins["data"]:
            if coin["nameid"] == coin_name.lower() or coin["symbol"].lower() == coin_name.lower():
                return coin
        return {}
    
    def convert_currency(self,usd_price,fiat_name):
        """
            convert_currency() method returns the converted price from USD to some other FIAT currency.
        """
        query = f"USD_{fiat_name.upper()}"
        url = f"https://free.currconv.com/api/v7/convert?q={query}&compact=ultra&apiKey={os.environ['CONVERT_API_KEY']}"
        fiat_price = requests.get(url).json()[query]
        return float(usd_price) * fiat_price

    def get_candles(self,coinname,chart_interval):
        """
            get_candles() method saves the specified coin's candlechart in the app directory 
            and host it in imgbb server and returns the JSON of that hosted image.
        """
        try:
            symbol = coinname.upper()
            candle.save_chart(symbol=symbol,interval=chart_interval)
            return self.host_snapshot("chart.png")
        except Exception as e:
            return e
    
    def host_snapshot(self,path):
        """
            host_snapshot() methods hosts the image to the imgbb server and returns the
            response as JSON.
        """
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
