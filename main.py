import requests
import json
import time
import sys
from datetime import datetime as dt
from proceduralMethods import *

flagSymbols = ["BTC_BRL"]
flagTimes = ["ONE_HOU"]
movingAverageWindows = [5, 10, 30, 60, 80]

while(1):
    time.sleep(1)
    for symbol in flagSymbols:
        try:
            historyRequest = requests.get("https://api.novadax.com/v1/market/kline/history?symbol={}&unit={}&from={}&to={}".format(
                symbol, flagTimes[0], int(dt.now().timestamp()-86400*30), int(dt.now().timestamp())))

            historyPrices = getHistoryPrices(historyRequest)

            momentRequest = requests.get(
                "https://api.novadax.com/v1/market/ticker?symbol={}".format(symbol))

            momentData = momentRequest.json()['data']

            verifyCrossedMAs(symbol, historyPrices, float(
                momentData["ask"]), movingAverageWindows)

        except NameError:
            print("Oops, there was a problem. Exiting...", NameError)
            sys.exit(1)
