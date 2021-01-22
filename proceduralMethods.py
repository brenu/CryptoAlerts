import math
import subprocess as s
import os

imagePath = os.path.abspath("logo.png")


def getHistoryPrices(rawData):
    historyData = rawData.json()['data']
    historyPrices = []

    for candle in historyData:
        historyPrices.append(candle["closePrice"])

    return historyPrices


def getMovingAverage(prices, window):
    separatedPrices = prices[-window:]
    movingAverage = sum(separatedPrices) / window

    return movingAverage


def getStandardDeviation(prices, average):
    itemsSum = 0
    pricesLength = 0
    for price in prices:
        pricesLength = pricesLength + 1
        itemsSum = itemsSum + ((price-average) ** 2)

    return math.sqrt(itemsSum/pricesLength)


def verifyLimit(limit, presentPrice, lastPrice):
    if limit > lastPrice and limit < presentPrice:
        return 1
    elif limit < lastPrice and limit > presentPrice:
        return 1
    else:
        return 0


def verifyBollingerBands(history, presentPrice, periods):
    movingAverage = getMovingAverage(history, periods)
    standardDeviation = getStandardDeviation(
        history[-periods:], movingAverage)

    upperBand = movingAverage + 2*standardDeviation
    lowerBand = movingAverage - 2*standardDeviation

    if upperBand < presentPrice and upperBand > history[-1]:
        return 1
    elif upperBand > presentPrice and upperBand < history[-1]:
        return -1
    elif lowerBand < presentPrice and lowerBand > history[-1]:
        return 2
    elif lowerBand > presentPrice and lowerBand < history[-1]:
        return -2
    else:
        return 0


def verifyCrossedMAs(history, presentPrice, window):
    movingAverage = getMovingAverage(history, window)
    if movingAverage < presentPrice and movingAverage > history[-1]:
        return 1
    elif movingAverage > presentPrice and movingAverage < history[-1]:
        return -1
    else:
        return 0


def showAlert(message):
    s.call(['notify-send', '-i', imagePath, '-t', '10000', 'CryptoAlerts',
            "<span color='#ddd' font='16px'><b>{}</b></span>".format(message)])


def printBanner():
    print("\n############################################################################")
    print("############################    CryptoAlerts   #############################")
    print("############################# 1.1 - by Exceed ##############################")
    print("############################################################################")


def printHelp():
    printBanner()
    print("\n\nThese are the flags you may use in order to configure your analysis environment. If you need more information about specific flags, see the README file.\n")
    print("-h or --help       List commands and examples\n")
    print("-s or --symbols    Set the verified cryptocurrencies using Novadax pattern\n                   and separating them using commas.\n                   Ex: CryptoAlerts.py -s BTC_BRL,ETH_BRL,OMG_EUR,ADA_USD\n")
    print("-t or --times      Set the times you would like to be advertised of, by\n                   by using Novadax pattern and separating using commas.\n                   Ex: CryptoAlerts.py -t FIFTEEN_MIN,ONE_HOU,ONE_DAY\n")
    print("-w or --windows    Set the windows you generally use for moving averages,\n                   and separate them using commas.\n                   Ex: CryptoAlerts.py -w 9,21,60,80\n")
    print("-l or --limits     Set limit prices you would like to be advertised of,\n                   separating them using commas.\n                   Ex: CryptoAlerts.py -l ETH_BRL,1300.18,BTC_BRL,110520.50\n")
    print("-b or --bollinger  Set the period for the Bollinger Bands, if you want to\n                   Ex: CryptoAlerts.py -b 20")
