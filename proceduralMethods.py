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


def verifyCrossedMAs(symbol, flagTime, history, presentPrice, movingAverageWindows):
    for window in movingAverageWindows:
        movingAverage = getMovingAverage(history, window)
        if movingAverage < presentPrice and movingAverage > history[-1]:
            print("O ativo {} cruzou a media móvel de {} para cima no gráfico {}".format(
                symbol, window, flagTime))
        elif movingAverage > presentPrice and movingAverage < history[-1]:
            print("O ativo {} cruzou a media móvel de {} para baixo no gráfico {}".format(
                symbol, window, flagTime))
