import requests, time, config
import yahoo_fin.stock_info as yf
from discord import Webhook, RequestsWebhookAdapter

webhook = Webhook.from_url(config.DIS_WEBHOOK_TELBOT, adapter=RequestsWebhookAdapter())
#webhook2 = Webhook.from_url(config.DIS_WEBHOOK_TEST, adapter=RequestsWebhookAdapter())

price =''
lastPrice =''

socket = config.SOCKET_DISCORD
bot_token = config.TOKEN_TEL_BOT
#bot_chatID = config.TEL_CHAT_AL
bot_chatID = config.TEL_CHAT_LE

alertList=[{
    #CW46
    "Ticker": 'SBGI',
    "Support": 26.04,
    "First Resistance": 26.68,
    "First Take Profit": 29.30,
    "Stop Loss": 25.60,
    "Swing Target": 30.00,
    "LastPrice": 0.000,
    "SupportTriggerU": time.time()-10000,
    "SupportTriggerD": time.time()-10000,
    "SupportTriggerP": time.time()-10000,
    "FirstResistanceTriggerU": time.time()-10000,
    "TakeProfitTriggerU": time.time()-10000,
    "StopLossTriggerD": time.time()-10000,
    "SwingTargetTriggerU": time.time()-10000
},{
    #CW46
    "Ticker": 'SE',
    "Support": 338.50,
    "First Resistance": 344.50,
    "First Take Profit": 367.50,
    "Stop Loss": 331.00,
    "Swing Target": 370.00,
    "LastPrice": 0.000,
    "SupportTriggerU": time.time()-10000,
    "SupportTriggerD": time.time()-10000,
    "SupportTriggerP": time.time()-10000,
    "FirstResistanceTriggerU": time.time()-10000,
    "TakeProfitTriggerU": time.time()-10000,
    "StopLossTriggerD": time.time()-10000,
    "SwingTargetTriggerU": time.time()-10000
},{
    #CW46
    "Ticker": 'UPWK',
    "Support": 46.50,
    "First Resistance": 52.00,
    "First Take Profit": 58.00,
    "Stop Loss": 43.30,
    "Swing Target": 60.00,
    "LastPrice": 0.000,
    "SupportTriggerU": time.time()-10000,
    "SupportTriggerD": time.time()-10000,
    "SupportTriggerP": time.time()-10000,
    "FirstResistanceTriggerU": time.time()-10000,
    "TakeProfitTriggerU": time.time()-10000,
    "StopLossTriggerD": time.time()-10000,
    "SwingTargetTriggerU": time.time()-10000
}]
def getStock():
     for dic in alertList:
        try:
            if dic["LastPrice"] == 0:
                dic["LastPrice"] = yf.get_live_price(dic["Ticker"]).round(3)
            price = yf.get_live_price(dic["Ticker"]).round(3)
            lastPrice = dic["LastPrice"]
            message = ''
            if price > dic["First Resistance"] and lastPrice < dic["First Resistance"] and time.time()-dic["FirstResistanceTriggerU"] >=3600:
                message = dic["Ticker"] + ' just broke through the first resistance (' + str(dic["First Resistance"]) + ')'
                dic["FirstResistanceTriggerU"] = time.time()
            elif price > dic["First Take Profit"] and lastPrice < dic["First Take Profit"] and time.time()-dic["TakeProfitTriggerU"] >=3600:
                message = dic["Ticker"] + ': Take first profits (' + str(dic["First Take Profit"]) + ')'
                dic["TakeProfitTriggerU"] = time.time()
            elif price > dic["Swing Target"] and lastPrice < dic["Swing Target"] and time.time()-dic["SwingTargetTriggerU"] >=3600:
                message = dic["Ticker"] + ' just reached the Swing Target (' + str(dic["Swing Target"]) + ')'
                dic["SwingTargetTriggerU"] = time.time()
            elif price > dic["Support"] and lastPrice < dic["Support"] and time.time()-dic["SupportTriggerU"] >=3600:
                message = dic["Ticker"] + ' just pushed through the Support (' + str(dic["Support"]) + ')'
                dic["SupportTriggerU"] = time.time()
            elif price < dic["Support"] and lastPrice > dic["Support"] and time.time()-dic["SupportTriggerD"] >=3600:
                message = dic["Ticker"] + ' just fell through support (' + str(dic["Support"]) + ')'
                dic["SupportTriggerD"] = time.time()
            elif price == dic["Support"] and time.time()-dic["SupportTriggerP"] >=3600:
                message = dic["Ticker"] + ' just reached support (' + str(dic["Support"]) + ')'
                dic["SupportTriggerP"] = time.time()
            elif price < dic["Stop Loss"] and lastPrice > dic["Stop Loss"] and time.time()-dic["StopLossTriggerD"] >=3600:
                message = dic["Ticker"] + ': Stop loss triggered (' + str(dic["Stop Loss"]) + ')'
                dic["StopLossTriggerD"] = time.time()
            dic["LastPrice"] = price
            if message != '':
                webhook.send(message)
                #webhook2.send(message)
                send_text='https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=HTML&text=' + message
                response=requests.get(send_text)
                print(message)
                print(response)
            #print('Old Price of ' + dic["Ticker"] + ': ' + str(lastPrice))
            #print('New Price of ' + dic["Ticker"] + ': ' + str(price))
        except Exception as e:
            print("OS error: {0}".format(e))
while True:
    getStock()
    time.sleep(15)