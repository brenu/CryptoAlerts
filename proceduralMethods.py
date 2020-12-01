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
