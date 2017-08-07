import urllib2
import json
import datetime

def get_prices_hourly(acao):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/" + acao + "?range=6mo&includePrePost=false&interval=1h&corsDomain=finance.yahoo.com&.tsrc=finance"    
    response = urllib2.urlopen(url)
    return load_prices(response.read())

def load_prices(data_str):    
    obj = json.loads(data_str)
    timestamp = obj["chart"]["result"][0]["timestamp"]
    quote = obj["chart"]["result"][0]["indicators"]["quote"][0]
    
    quote_open = quote["open"]
    quote_close = quote["close"]
    quote_low = quote["low"]
    quote_high = quote["high"]
    
    items = []
    total = len(timestamp)
    for x in xrange(0, total):
        items.append({ 
            "date": datetime.datetime.fromtimestamp(timestamp[x]), 
            "open": quote_open[x],
            "close": quote_close[x],
            "low": quote_low[x],
            "high": quote_high[x]
        })
    return items

def analyse(prices, days):
    total = len(prices)
    buys = []
    sells = []
    
    for x in xrange(0, total):
        current = prices[x]
        if x >= (days + 1):
            resistence = max([p["close"] for p in prices[x - days - 1: x - 1]])
            suport = min([p["close"] for p in prices[x - days - 1: x - 1]])
            if current["close"] > resistence:
                if len(buys) <= len(sells):
                    buys.append(current)
            else:
                if len(buys) > len(sells):
                    sells.append(current)
    
    if len(sells) < len(buys):
        sells.append(prices[-1])
        
    return calculate(buys, sells)

def calculate(buys, sells):
    saldo = 100000
    total = len(buys)
    for x in xrange(0, total):
        buy = buys[x]
        sell = sells[x]
        
        saldo *= sell["close"] / buy["close"]
    return saldo / 100000

def summary(acao):
    prices = get_prices_hourly(acao)
    x = [(x,analyse(prices, x)) for x in range(1, 90)]
    a = sorted(x, key=lambda t: -t[1])
    return a
    
    
    
    
    
    