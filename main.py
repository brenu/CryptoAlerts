import requests
import json
from datetime import datetime as dt

flagSymbol = "BTC_BRL"
flagTime = "ONE_HOU"

r = requests.get("https://api.novadax.com/v1/market/tickers")

data = r.json()['data']
biggerSymbol = 0

for item in data:
    symbolLength = len(item['symbol'])

    if symbolLength > biggerSymbol:
        biggerSymbol = symbolLength

for item in data:
    price = item['ask']

    symbol = item['symbol']
    symbolLength = len(symbol)

    print("Symbol: ", symbol, "{}|  Actual price:".format(
        " "*(biggerSymbol-symbolLength) if symbolLength < biggerSymbol else ""), price)
