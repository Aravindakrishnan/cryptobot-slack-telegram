import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask , Response , request
import requests
import slack 
from slackeventsapi import SlackEventAdapter
from utils.crypto import Crypto
import json
# intialization
ENV_PATH= Path(".") / ".env"
load_dotenv(dotenv_path=ENV_PATH)

app = Flask(__name__)

PORT = 5001

slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET_TOKEN"],'/events',app)
bot = slack.WebClient(token=os.environ["BOT_TOKEN"])
BOT_ID = bot.api_call("auth.test")["user_id"]

@app.route("/")
def index():
    return "Hey There! I'm Cryptobot"

@app.route("/getprice",methods=["POST"])
def get_price():
    """
        get_price() method return the price of the particular coin 
        eg : [Coinname] : [Price]
    """
    crypto = Crypto()
    data = request.form
    channel_id = data.get('channel_id')
    coin_name,*fiat_options = data.get("text").split()
    coin = crypto.get_coin(coin_name)

    if(not fiat_options):
        text = f"{coin['name']} : {coin['price_usd']} $"
    else:
        price = crypto.convert_currency(coin['price_usd'],fiat_options[0])
        text = f"{coin['name']} : {price}"
    bot.chat_postMessage(channel=channel_id,text=text)
    return Response(), 200

@app.route("/showdetail",methods=["POST"])
def show_detail():
    """
        show_detail() method return the detail view of particular coin. 
    """
    data = request.form
    channel_id = data.get('channel_id')
    coin_name,*fiat_options = data.get("text").split()
    crypto = Crypto()
    coin = crypto.get_coin(coin_name)
    
    if(not fiat_options):
        price = f"{coin['price_usd']} USD"
    else:
        price = f"{crypto.convert_currency(coin['price_usd'],fiat_options[0])} {fiat_options[0].upper()}"

    text = f"""----------------------------------------------------
                        {coin["name"]}
----------------------------------------------------
        id : {coin["id"]} 
        rank : {coin["rank"]}
        name : {coin["name"]}
        price : {price}
        1h_percentage: {coin["percent_change_1h"]}  
        1d_percentage : {coin["percent_change_24h"]} 
        7d_percentage : {coin["percent_change_7d"]} 
        market_cap : {coin["market_cap_usd"]}
-----------------------------------------------------
    """
    bot.chat_postMessage(channel=channel_id,text=text)
    return Response(), 200

@app.route("/showcandle",methods=["POST"])
def show_candle():
    """
        show_candle() return the snapshot of the coin graph at particular time_frame
        [1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M]
    """
    crypto = Crypto()
    data = request.form
    channel_id = data.get('channel_id')
    coin_name,*time_options = data.get("text").split()
    coin = crypto.get_coin(coin_name)   

    if(not time_options):
        time_options = ["1d"] #default

    response = crypto.get_candles(coin["symbol"],time_options[0])
    bot.chat_postMessage(channel=channel_id,text="",attachments=[{"text":f"{coin['name']} {time_options[0]} graph 📈","image_url" : response["data"]["url"]}])
    return Response(), 200

@app.route("/help",methods=["POST"])
def show_help():
    data = request.form
    channel_id = data.get('channel_id')
    text = """
        Slash Commands :

        /getprice [coin_name or coin_symbol] [fiat_name] - returns default USD
        /getprice [coin_name or coin_symbol] [fiat_name] returns based on fiat

        /showdetail [coin_name or coin_symbol] [fiat_name] returns detail view of coin default : USD
        /showdetail [coin_name or coin_symbol] [fiat_name] returns detail view of coin based on fiat
       
        /showcandle [coin_name or coin_symbol] - returns default : 1d graph   
        /showcandle [coin_name or coin_symbol] [1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M] - returns graph based on time_frame 
    
        doc : https://cryptobotdocs.netlify.app
    """
    bot.chat_postMessage(channel=channel_id,text=text)
    return Response(),200

    
if __name__ == "__main__":
    app.run(debug=True,port=PORT)
