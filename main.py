import requests
import json
import time
import sys
import getopt
from datetime import datetime as dt
from proceduralMethods import *
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

options, remaining = getopt.gnu_getopt(
    sys.argv[1:], 's:t:w:l:h', ['symbols=', 'times=', 'windows=', 'help=', 'limit='])

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

                wasLimitCrossed = verifyLimit(
                    limits[symbol], float(momentData['ask']), float(historyPrices[-1]))

                if wasLimitCrossed == 1 and alertsRegister[symbol]["limit"].alertDirection == 0:
                    s.call(['notify-send', '-i', '/home/exceed/Documents/projetos/CryptoAlerts/here.png', '-t', '10000', 'CryptoAlerts', "<span color='#ddd' font='16px'><i><b>O ativo {} cruzou o limite de {}</b></i></span>".format(
                            symbol, limits[symbol])])
                    alertsRegister[symbol]["limit"].alertDirection = 1

                for window in movingAverageWindows:
                    crossedMAs = verifyCrossedMAs(historyPrices, float(
                        momentData["ask"]), window)
                    if crossedMAs == 1 and alertsRegister[symbol]["windows"][window].alertDirection != 1:
                        s.call(['notify-send', '-i', '/home/exceed/Documents/projetos/CryptoAlerts/here.png', '-t', '10000', 'CryptoAlerts', "<span color='#ddd' font='16px'><i><b>O ativo {} cruzou a media móvel de {} para cima no gráfico {}</b></i></span>".format(
                            symbol, window, flagTime)])
                        alertsRegister[symbol]["windows"][window].alertDirection = 1
                    elif crossedMAs == -1 and alertsRegister[symbol]["windows"][window].alertDirection != -1:
                        s.call(['notify-send', '-i', '/home/exceed/Documents/projetos/CryptoAlerts/here.png', '-t', '10000', 'CryptoAlerts', "<span color='#ddd' font='16px'><b>O ativo {} cruzou a media móvel de {} para baixo no gráfico {}</b></span>".format(
                            symbol, window, flagTime)])
                        alertsRegister[symbol]["windows"][window].alertDirection = -1
            except NameError:
                print("Oops, there was a problem. Exiting...", NameError)
                sys.exit(1)
