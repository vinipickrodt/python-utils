import sys
import urllib2
import json
import datetime

def get_prices(acao, interval = "1h", range = "6m"):
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/" + acao + "?range=" + range + "&includePrePost=false&interval=" + interval + "&corsDomain=finance.yahoo.com&.tsrc=finance"    
        response = urllib2.urlopen(url)
        return load_prices(response.read())
    except:
        print "URL: " + url
        pass

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
        if quote_close[x] > 0:
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
    stop_gain = 0
    
    for x in xrange(0, total):
        current = prices[x]
        if x >= (days + 1):
            resistence = max([p["close"] for p in prices[x - days - 1: x - 1]])
            suport = min([p["close"] for p in prices[x - days - 1: x - 1]])
            esta_comprado = len(buys) > len(sells)
            quebrou_resistencia = current["close"] > resistence
            comprar = not esta_comprado and quebrou_resistencia
            vender = esta_comprado and (not quebrou_resistencia) or (stop_gain > 0 and current["low"] <= stop_gain)
            
            if comprar:
                buys.append(current)
            elif vender:
                preco = current.copy()
                if stop_gain > 0:
                    preco["close"] = stop_gain
                sells.append(preco)
                stop_gain = 0
            
            if len(buys) > 0 and current["close"] > buys[-1]["close"]:
                stop_gain = current["close"]
    
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

def summary(acao, _interval = "1d", _range = "5y"):
    prices = get_prices(acao, _interval, _range)
    temp = [(x, analyse(prices, x)) for x in range(1, 90)]
    a = sorted(temp, key = lambda t: -t[1])
    return a

result = None
if len(sys.argv) >= 4:
    result = summary(sys.argv[1], sys.argv[2], sys.argv[3])
elif len(sys.argv) >= 3:
    result = summary(sys.argv[1], sys.argv[2])
elif len(sys.argv) >= 2:
    result = summary(sys.argv[1])

if result is None:
    print "finance.py acao"
else:
    #print str(result)
    print "\n".join([ str(v) for v in result[0:10] ])







