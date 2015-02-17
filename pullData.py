#!/usr/local/bin/python
from yahoo_finance import Share

import argparse
import datetime
import time

parser = argparse.ArgumentParser(description='Pull stock price from Yahoo! Finance')
parser.add_argument('-c','--code', help='stock code',required=True)
args = parser.parse_args()


stock = Share(args.code)

today = datetime.date.today()
print (time.strftime("%Y-%m-%d"))
ts = stock.get_historical('2014-01-01',today.strftime("%Y-%m-%d"))

filew = open('db/' + args.code + '.txt', 'w')

# save to file in OHLC format
for eachDay in ts:
   filew.write(eachDay['Date'] + ',' + eachDay['Open'] + ',' + eachDay['High'] + "," + eachDay['Low'] + ',' + eachDay['Close'] + "\n")

filew.close()
print "done"
