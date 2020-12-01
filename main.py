import requests
import json
import time
import sys
import getopt
from datetime import datetime as dt
from proceduralMethods import *


class AlertStorage:
    def __init__(self, alertType, alertDirection):
        self.type = alertType
        self.alertDirection = alertDirection


flagSymbols = ["BTC_BRL"]
flagTimes = ["ONE_HOU"]
movingAverageWindows = [9]

options, remaining = getopt.gnu_getopt(
    sys.argv[1:], 's:t:w:', ['symbols=', 'times=', 'windows='])

for opt, arg in options:
    if opt in ('-s', '--symbols'):
        flagSymbols = arg.split(',')
    elif opt in ('-t', '--times'):
        flagTimes = arg.split(',')
    elif opt in ('-w', '--windows'):
        movingAverageWindows = list(map(int, arg.split(',')))

alertsRegister = {}
for symbol in flagSymbols:
    alertsRegister[symbol] = {}
    for window in movingAverageWindows:
        alertsRegister[symbol][window] = AlertStorage('MA', 0)

while(1):
    time.sleep(1)
    for symbol in flagSymbols:
        for flagTime in flagTimes:
            try:
                historyRequest = requests.get("https://api.novadax.com/v1/market/kline/history?symbol={}&unit={}&from={}&to={}".format(
                    symbol, flagTime, int(dt.now().timestamp()-86400*30), int(dt.now().timestamp())))

                historyPrices = getHistoryPrices(historyRequest)

                momentRequest = requests.get(
                    "https://api.novadax.com/v1/market/ticker?symbol={}".format(symbol))

                momentData = momentRequest.json()['data']

                for window in movingAverageWindows:
                    crossedMAs = verifyCrossedMAs(historyPrices, float(
                        momentData["ask"]), window)

                    if crossedMAs == 1 and alertsRegister[symbol][window] != 1:
                        print("O ativo {} cruzou a media móvel de {} para cima no gráfico {}".format(
                            symbol, window, flagTime))
                        alertsRegister[window] = 1
                    elif crossedMAs == -1 and alertsRegister[symbol][window] != 1:
                        print("O ativo {} cruzou a media móvel de {} para baixo no gráfico {}".format(
                            symbol, window, flagTime))
                        alertsRegister[window] = -1
            except NameError:
                print("Oops, there was a problem. Exiting...", NameError)
                sys.exit(1)
