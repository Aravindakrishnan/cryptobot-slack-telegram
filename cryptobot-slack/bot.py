import slack 
import os
from pathlib import Path
from dotenv import load_dotenv
from crypto import Crypto
from flask import Flask , Response , request
from slackeventsapi import SlackEventAdapter

ENV_PATH= Path(".") / ".env"
load_dotenv(dotenv_path=ENV_PATH)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET_TOKEN"],'/events',app)
bot = slack.WebClient(token=os.environ["BOT_TOKEN"])
BOT_ID = bot.api_call("auth.test")["user_id"]

@app.route("/getprice",methods=["POST"])
def get_price():
    data = request.form
    coin_name,*fiat_options = data.get("text").split()
    coin = Crypto().get_coin(coin_name)

    if(not fiat_options):
        text = f"{coin['name']} : {coin['price_usd']} $"
    else:
        price = Crypto().convert_currency(coin['price_usd'],fiat_options[0])
        text = f"{coin['name']} : {price}"
    
    bot.chat_postMessage(channel="#crypto",text=text)
    return Response(), 200

@app.route("/showdetail",methods=["POST"])
def show_detail():
    data = request.form
    coin_name,*fiat_options = data.get("text").split()
    coin = Crypto().get_coin(coin_name)
    
    if(not fiat_options):
        price = f"{coin['price_usd']} USD"
    else:
        price = f"{Crypto().convert_currency(coin['price_usd'],fiat_options[0])} {fiat_options[0].upper()}"

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

if __name__ == "__main__":
    app.run(debug=True,port=5500)
