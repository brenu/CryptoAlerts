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
