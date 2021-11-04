import os
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask , Response , request
import slack 
from slackeventsapi import SlackEventAdapter

from utils.crypto import Crypto
from utils.chart import get_chart_id

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
    crypto = Crypto()
    data = request.form
    coin_name,*fiat_options = data.get("text").split()
    coin = crypto.get_coin(coin_name)

    if(not fiat_options):
        text = f"{coin['name']} : {coin['price_usd']} $"
    else:
        price = crypto.convert_currency(coin['price_usd'],fiat_options[0])
        text = f"{coin['name']} : {price}"

    bot.chat_postMessage(channel="#crypto",text=text)
    return Response(), 200

@app.route("/showdetail",methods=["POST"])
def show_detail():
    data = request.form
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
    bot.chat_postMessage(channel="#crypto",text=text)
    return Response(), 200
    
@app.route("/showgraph",methods=["POST"])
def show_graph():
    crypto = Crypto()
    data = request.form
    coin_name,*time_options = data.get("text").split()
    coin = crypto.get_coin(coin_name)   

    if(not time_options):
        time_options = ["1d"] #default

    
    if(not get_chart_id(time_options[0])):
        bot.chat_postMessage(channel="#crypto",text="Kindly check the input please!")
        return Response(),400
    response = crypto.take_snapshot(coin["nameid"],time_options[0])
    bot.chat_postMessage(channel="#crypto",text="",attachments=[{"text":f"{coin['name']} {time_options[0]} graph 📈","image_url" : response["data"]["url"]}])
    return Response(), 200


    
if __name__ == "__main__":
    app.run(debug=True,port=PORT)
