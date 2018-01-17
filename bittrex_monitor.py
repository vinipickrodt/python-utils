'''
pip install python-bittrex
pip install win10toast
'''

import winsound, sys, signal, time, os
from bittrex.bittrex import Bittrex, API_V2_0
from win10toast import ToastNotifier
toaster = ToastNotifier()
			  
b = Bittrex(None, None)
vars = None #price variations
initialPrices = None

#config
NOTIFICATION_PERCENT = 0.03 #variation to notify

while True:
	markets = ["USDT-BTC", "USDT-ETH", "BTC-FTC"]

	print ("Updating Prices...")
	currentPrices = [ b.get_ticker(m)["result"]["Last"] for m in markets ]
	initialPrices = currentPrices[:] if initialPrices is None else initialPrices

	os.system("cls")
	
	changes = []
	for x in xrange(0, len(markets)):
		market = markets[x]
		prev_var = 0 if vars is None else vars[x]
		price = currentPrices[x]
		initial_price = initialPrices[x]
		
		varPercent = "{0:.2f}".format((price / initial_price - 1) * 100) + "%"
		varPercent = ("+" if price > initial_price else "") + varPercent
		
		print (market + " = " + "{0:.10f}".format(price) + " (" + varPercent + ")")
		
		if prev_var <= 0 or abs(max(prev_var, price) / min(prev_var, price) - 1) > NOTIFICATION_PERCENT:
			changes.append(market + " = " + "{0:.10f}".format(price) + " (" + varPercent + ")")
			if vars is None:
				vars = [None] * len(markets)
			vars[x] = price
	
	if len(changes) > 0:
		winsound.Beep(1500, 300)
		toaster.show_toast("Price Alert", "\r\n".join(changes), duration = 5)
	
	time.sleep(5)

'''
TODOS

-- Try....
from PyQt5 import Qt
import sys
app = Qt.QApplication(sys.argv)
systemtray_icon = Qt.QSystemTrayIcon(app, Qt.QIcon('/path/to/image'))
systemtray_icon.show()
systemtray_icon.showMessage('Title', 'Content')


-- TEST on Windows..
def sigint_handler(signum, frame):
    sys.exit(-1)

signal.signal(signal.SIGINT, sigint_handler)
'''
