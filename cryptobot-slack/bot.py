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
    coin = Crypto().get_coin(data.get(coin_name))

    if(not fiat_options):
        text = f"{coin['name']} : {coin['price_usd']} $"
    else:
        price = Crypto().convert_currency(coin['price_usd'],fiat_options[0])
        text = f"{coin['name']} : {price}"
    
    bot.chat_postMessage(channel="#crypto",text=text)
    return Response(), 200
    
if __name__ == "__main__":
    app.run(debug=True,port=5500)
