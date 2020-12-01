def getHistoryPrices(rawData):
    historyData = rawData.json()['data']
    historyPrices = []

    for candle in historyData:
        historyPrices.append(candle["closePrice"])

    return historyPrices


def getMovingAverage(prices, window):
    pricesLength = len(prices)
    start = pricesLength-window-1
    separatedPrices = prices[start:-1]

    movingAverage = sum(separatedPrices) / window

    return movingAverage


def verifyCrossedMAs(history, presentPrice, window):
    movingAverage = getMovingAverage(history, window)
    if movingAverage < presentPrice and movingAverage > history[-1]:
        return 1
    elif movingAverage > presentPrice and movingAverage < history[-1]:
        return -1
    else:
        return 0


def printBanner():
    banner = 0


def printHelp():
    printBanner()
    print("\n\nThese are the flags you may use in order to configure your analysis environment. If you need more information about specific flags, see the README file.\n")
    print("-h or --help       List commands and examples\n")
    print("-s or --symbols    Set the verified cryptocurrencies using Novadax pattern\n                   and separating them using commas.\n                   Ex: CryptoAlerts.py -s BTC_BRL,ETH_BRL,OMG_EUR,ADA_USD\n")
    print("-t or --times      Set the times you would like to be advertised of, by\n                   by using Novadax pattern and separating using commas.\n                   Ex: CryptoAlerts.py -t FIFTEEN_MIN,ONE_HOU,ONE_DAY\n")
    print("-w or --windows    Set the windows you generally use for moving averages,\n                   and separate them using commas.\n                   Ex: CryptoAlerts.py -w 9,21,60,80")
