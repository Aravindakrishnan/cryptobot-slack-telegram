import requests

class Crypto:
    def __init__(self):
        url = "https://api.coinlore.net/api/tickers/?limit=2054"
        self.coins = requests.get(url).json()    
    
    def get_coins(self):
        return self.coins

    def get_coin(self,coin_name):
        coin_detail = {}
        for coin in self.coins["data"]:
            if(coin["nameid"] == coin_name.lower() or coin["symbol"].lower() == coin_name.lower()):
                coin_detail = coin
                break
        return coin_detail

    