# cryptobot-slack-telegram

Cryptobot is the slackbot used for getting info about the cryptocurrencies 💰

[documentation](https://cryptobotdocs.netlify.app/)

![logo_.png](https://github.com/Aravindakrishnan/cryptobot-slack-telegram/blob/main/doc/icon/logo_.png)

# Step by Step Implementation [DONE ✅]:

clone the repository and get into cryptobot-slack directory and .

```
git clone https://github.com/Aravindakrishnan/cryptobot-slack-telegram
```

create a .env file and put essential API keys

```
BOT_TOKEN=XXXXXXX-XXXXXXXXX-XXXXXXXX
SIGNING_SECRET_TOKEN=XXXXXXXXXXX
IMGBB_API_KEY=XXXXXXXXXXX
CONVERT_API_KEY=XXXXXXXXXXX
```

#### API resources are ,

[Slack_API](https://api.slack.com/)

[Imgbb_API](https://api.imgbb.com/)

[Currency_Converter_API](https://free.currencyconverterapi.com/free-api-key)

# Installation of ngrok

[download_ngrok](https://ngrok.com/download)

# Running the bot

* step1 : create a bot app in slack and add bot to your workspace.

* step2 : copy paste needed API_KEYS in .env file.

* step3 : install required libs and run bot.py python script.

```
pip install -r requirements.txt
python3 bot.py
```

* step4 : create a ngrok server

```
ngrok http [PORT]
```

* step5 : copy https:// link generated by ngrok.

* step6 : Paste it in event_subscriptions and slash_command.

* step7 : head towards installAPP and reinstall the app.

## Usage : Slack Bot Methods 

- /getprice [coin_name or coin_symbol] - returns the current price of the coin default : USD
- /getprice [coin_name or coin_symbol] [fiat_name] - returns the current price of the coin in fiat.

- /showdetail [coin_name or coin_symbol] - returns the complete detail about the selected cryptocurrency.
- /showdetail [coin_name or coin_symbol] - returns the complete detail about the current cryptocurrency with specific fiat price.

- /showgraph [coin_name or coin_symbol] - returns the candle graph snapshot of the particular coin.
- /showgraph [coin_name or coin_symbol] [1d,7d,1m,3m,1y,ytd,all] - return the candle graph snapshot of the particular coin like 1day candle_graph , 7days candle_graph etc.,

### Examples :

```
/getprice btc inr
```

```
/showdetail btc inr
```

```
/showgraph btc 1y
```

### Sample Outputs

/getprice

![getprice.png](https://github.com/Aravindakrishnan/cryptobot-slack-telegram/blob/main/doc/images/getprice.png)

/showdetail

![showdetail.png](https://github.com/Aravindakrishnan/cryptobot-slack-telegram/blob/main/doc/images/showdetail.png)

/showcandle 

![showdetail01.png](https://github.com/Aravindakrishnan/cryptobot-slack-telegram/blob/main/doc/images/showgraph01.png)

![showdetail02.png](https://github.com/Aravindakrishnan/cryptobot-slack-telegram/blob/main/doc/images/showgraph02.png)