import os
import telebot
from utils.crypto import Crypto
from dotenv import load_dotenv
from pathlib import Path

# Commented it for hosting in ec2 server 

# TODO: uncomment it and create a .env in current directory.
# Paste needed API_KEYS ref : README.md

# ENV_PATH= Path(".") / ".env"
# load_dotenv(dotenv_path=ENV_PATH)

bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"])

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    """
        handle_start_help() - handles the /start and /help command
    """
    text = """
Here are the set of commands you can play 🕹️ with  :

        /getprice [coin_name or coin_symbol] [fiat_name] - returns default USD
        /getprice [coin_name or coin_symbol] [fiat_name] returns based on fiat

        /showdetail [coin_name or coin_symbol] [fiat_name] returns detail view of coin default : USD
        /showdetail [coin_name or coin_symbol] [fiat_name] returns detail view of coin based on fiat
       
        /showcandle [coin_name or coin_symbol] - returns default : 1d graph   
        /showcandle [coin_name or coin_symbol] [1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M] - returns graph based on time_frame 
    
doc : https://cryptobotdocs.netlify.app
    """    
    print(message)
    user = message.from_user
    full_name = f"{user.first_name} {user.last_name}"
    bot.reply_to(message, f"Hey {full_name} how you doing?\n {text}")

@bot.message_handler(commands=['getprice'])
def handle_getprice(message):
    """
        handle_getprice() method return the price of the particular coin 
        eg : [Coinname] [Coinsymbol] : [Price]
    """
    crypto = Crypto()
    item = message.text.split()
    coinname,*fiat_option = item[1:]
    coin = crypto.get_coin(coinname)

    if(not fiat_option):
        price = coin['price_usd']  
        text = f"{coin['name']} [{coin['symbol']}] : {price} USD"      
    else:
        price = crypto.convert_currency(coin['price_usd'],fiat_option[0])
        text = f"{coin['name']} [{coin['symbol']}] : {price} {fiat_option[0].upper()}"
    
    bot.reply_to(message, text)

@bot.message_handler(commands=['showdetail'])
def handle_showdetail(message):
    """
        handle_showdetail() method return the detail view of particular coin. 
    """
    coin_name,*fiat_options = message.text.split()[1:]
    crypto = Crypto()
    coin = crypto.get_coin(coin_name)
    
    get_indicator = lambda x : "📈" if(float(x) > 0) else "📉"

    if(not fiat_options):
        price = f"{coin['price_usd']} USD"
    else:
        price = crypto.convert_currency(coin["price_usd"],fiat_options[0])
        price = f"{price} {fiat_options[0].upper()}"
    text = f"""----------------------------------------------------
                        {coin["name"]}
----------------------------------------------------
        id : {coin["id"]} 
        rank : {coin["rank"]}
        name : {coin["name"]}
        price : {price}
        1h_percentage: {coin["percent_change_1h"]} {get_indicator(coin["percent_change_1h"])}  
        1d_percentage : {coin["percent_change_24h"]} {get_indicator(coin["percent_change_24h"])} 
        7d_percentage : {coin["percent_change_7d"]} {get_indicator(coin["percent_change_7d"])} 
        market_cap : {coin["market_cap_usd"]}
----------------------------------------------------
    """
    bot.reply_to(message, text)

@bot.message_handler(commands=['showcandle'])
def handle_showcandle(message):
    """
        handle_showcandle() return the snapshot of the coin graph at particular time_frame
        [1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M]
    """
    chat_id = message.chat.id
    crypto = Crypto()
    coin_name,*time_options = message.text.split()[1:]
    coin = crypto.get_coin(coin_name)   

    if(not time_options):
        time_options = ["1d"] #default

    response = crypto.get_candles(coin["symbol"],time_options[0])
    try:
        bot.reply_to(message,f"{coin['name']} {coin['symbol']} {time_options[0]} is here 😉💰")
        bot.send_photo(chat_id,response["data"]["url"])
    except:
        bot.reply_to(message,"Oops..😕 Something went wrong!")
     
print("listening...") #for debug
bot.polling()