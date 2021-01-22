import requests
import json
import time
import sys
import getopt
from datetime import datetime as dt
from proceduralMethods import *
from helpers import *
import subprocess as s


class AlertStorage:
    def __init__(self, alertType, alertDirection):
        self.type = alertType
        self.alertDirection = alertDirection


flagSymbols = ["BTC_BRL"]
flagTimes = ["ONE_HOU"]
movingAverageWindows = [9]
hasLimit = False
limits = {}
bollingerPeriods = 0

options, remaining = getopt.gnu_getopt(
    sys.argv[1:], 's:t:w:l:b:h', ['symbols=', 'times=', 'windows=', 'limit=', 'bollinger=', 'help=', ])

for opt, arg in options:
    if opt in ('-s', '--symbols'):
        flagSymbols = arg.split(',')

    elif opt in ('-t', '--times'):
        flagTimes = arg.split(',')

    elif opt in ('-w', '--windows'):
        movingAverageWindows = list(map(int, arg.split(',')))

    elif opt in ('-l', '--limit'):
        args = arg.split(',')
        if len(args) % 2 != 0:
            print(
                '\nRequisição incorreta para a flag -l. Use o comando help para melhor informação')
        hasLimit = True
        for i in range(0, len(args)-1, 2):
            limits[args[i]] = float(args[i+1])

    elif opt in ('-b', '--bollinger'):
        if arg.isnumeric():
            bollingerPeriods = int(arg) if int(arg) > 0 else 0

    elif opt in ('-h', '--help'):
        printHelp()
        sys.exit(1)

alertsRegister = {}
for symbol in flagSymbols:
    alertsRegister[symbol] = {
        "windows": {},
    }
    for window in movingAverageWindows:
        alertsRegister[symbol]["windows"][window] = AlertStorage('MA', 0)
    alertsRegister[symbol]["limit"] = AlertStorage('LT', 0)
    alertsRegister[symbol]["bollingerBands"] = AlertStorage("BB", 0)

while(1):
    time.sleep(1)
    for symbol in flagSymbols:
        for flagTime in flagTimes:
            try:
                historyRequest = requests.get("https://api.novadax.com/v1/market/kline/history?symbol={}&unit={}&from={}&to={}".format(
                    symbol, flagTime, int(dt.now().timestamp()-timestamps[flagTime]*100), int(dt.now().timestamp())))

                historyPrices = getHistoryPrices(historyRequest)

                momentRequest = requests.get(
                    "https://api.novadax.com/v1/market/ticker?symbol={}".format(symbol))

                momentData = momentRequest.json()['data']

                if bollingerPeriods > 0:
                    wereBollingerBandsCrossed = verifyBollingerBands(
                        historyPrices, float(momentData['ask']), bollingerPeriods)

                    if wereBollingerBandsCrossed == 1 and alertsRegister[symbol]["bollingerBands"].alertDirection != 1:
                        showAlert("O ativo {} cruzou a BB superior de {} para cima no gráfico {}".format(
                            symbol, bollingerPeriods, flagTime))
                        alertsRegister[symbol]["bollingerBands"].alertDirection = 1
                    elif wereBollingerBandsCrossed == -1 and alertsRegister[symbol]["bollingerBands"].alertDirection != -1:
                        showAlert("O ativo {} cruzou a BB superior de {} para baixo no gráfico {}".format(
                            symbol, bollingerPeriods, flagTime))
                        alertsRegister[symbol]["bollingerBands"].alertDirection = -1
                    elif wereBollingerBandsCrossed == 2 and alertsRegister[symbol]["bollingerBands"].alertDirection != -2:
                        showAlert("O ativo {} cruzou a BB inferior de {} para cima no gráfico {}".format(
                            symbol, bollingerPeriods, flagTime))
                        alertsRegister[symbol]["bollingerBands"].alertDirection = 2
                    elif wereBollingerBandsCrossed == -2 and alertsRegister[symbol]["bollingerBands"].alertDirection != -2:
                        showAlert("O ativo {} cruzou a BB inferior de {} para baixo no gráfico {}".format(
                            symbol, bollingerPeriods, flagTime))
                        alertsRegister[symbol]["bollingerBands"].alertDirection = -2

                if symbol in limits:
                    wasLimitCrossed = verifyLimit(
                        limits[symbol], float(momentData['ask']), float(historyPrices[-1]))

                    if wasLimitCrossed == 1 and alertsRegister[symbol]["limit"].alertDirection == 0:
                        showAlert("O ativo {} cruzou o limite de {}".format(
                            symbol, limits[symbol]))
                        alertsRegister[symbol]["limit"].alertDirection = 1

                for window in movingAverageWindows:
                    crossedMAs = verifyCrossedMAs(historyPrices, float(
                        momentData["ask"]), window)
                    if crossedMAs == 1 and alertsRegister[symbol]["windows"][window].alertDirection != 1:
                        showAlert("O ativo {} cruzou a media móvel de {} para cima no gráfico {}".format(
                            symbol, window, flagTime))
                        alertsRegister[symbol]["windows"][window].alertDirection = 1
                    elif crossedMAs == -1 and alertsRegister[symbol]["windows"][window].alertDirection != -1:
                        showAlert("O ativo {} cruzou a media móvel de {} para baixo no gráfico {}".format(
                            symbol, window, flagTime))
                        alertsRegister[symbol]["windows"][window].alertDirection = -1
            except NameError:
                print("Oops, there was a problem. Exiting...", NameError)
                sys.exit(1)
