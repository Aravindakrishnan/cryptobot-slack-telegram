import requests

class Crypto:
    def __init__(self):
        url = "https://api.coinlore.net/api/tickers/?limit=2054"
        self.coins = requests.get(url).json()    
    
    def get_coins(self):
        return self.coins

    def get_coin(self,coin_name):
        for coin in self.coins["data"]:
            if coin["nameid"] == coin_name.lower() or coin["symbol"].lower() == coin_name.lower():
                return coin
        return {}
    
    def convert_currency(self,usd_price,fiat_name):
        query = f"USD_{fiat_name}"
        url = f"https://free.currconv.com/api/v7/convert?q={query}&compact=ultra&apiKey=b9e409f547a823042d5c"
        fiat_price = requests.get(url).json()[query]
        return usd_price * fiat_price
