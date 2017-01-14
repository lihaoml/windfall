#!/usr/local/bin/python

from yahoo_finance import Share

import argparse
import datetime, time
from datetime import timedelta

import sqlite3 as lite
import pandas
from google_finance import google_hist_price

class MarketDataStore:
   """ Storing and retrieving market data from database (SQLite)

   """
   def __init__(self, db_path):
      self.con = lite.connect(db_path)
      self.cur = self.con.cursor()
      # self.hist_data_tablename = 'HIST_DATA'
      self.hist_data_yahoo_tablename = 'HIST_DATA_YAHOO'
      self.hist_data_google_tablename = 'HIST_DATA_GOOGLE'
      self.stock_tablename = 'STOCK'

   def __del__(self):
      self.con.close()

   def append_hist_data(self, stock_sym_list):
      """       
      """
      today = datetime.date.today()
      for symbol in stock_sym_list:
         print ("pulling " + symbol)

         ### retrieve data from yahoo ################
         stock = Share(symbol)
         last_date = self.get_last_date(self.hist_data_yahoo_tablename, symbol)
         print last_date
         # filter out the strings in the returned list
         ts_ = [t for t in stock.get_historical(last_date.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")) if type(t) != type("")]
         ts = [t for t in ts_ if t['Date'] == t['Date']] # check that date is not nan
         # when there is no data to retrieve, get_historical returns a list of strings where each string is the column name
         # when there is data, get_historical returns a list of dict
         if len(ts) > 0:
            df = pandas.DataFrame(ts).set_index(['Symbol', 'Date'], drop=True, append=False, verify_integrity = True)
            print df
            df.to_sql(self.hist_data_yahoo_tablename, self.con, schema=None, if_exists='append', index=True, index_label=['Symbol', 'Date'])
         else:
            print "Yahoo %s: no new data to be added from %s to %s"%(symbol, last_date, today)

         ### retrieve data from google ###############
         last_date = self.get_last_date(self.hist_data_google_tablename, symbol)
         df2 = google_hist_price(symbol, (last_date+timedelta(1)).strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))
         if not(df2.empty):
            print df2
            df2.to_sql(self.hist_data_google_tablename, self.con, schema=None, if_exists='append', index=True, index_label=['Symbol', 'Date'])
         else:
            print "Google %s: no new data to be added from %s to %s"%(symbol, last_date, today)

         time.sleep(5)
         
   def get_last_date(self, tablename, symbol):
      try:
         command_str = "SELECT DATE FROM %s where symbol = '%s'"%(tablename, symbol)
         self.cur.execute(command_str)
         rows = self.cur.fetchall()
         return datetime.datetime.strptime(max([n[0].encode() for n in rows]), "%Y-%m-%d").date()
      except:
         return datetime.date(1990, 1, 1)

   def get_hist_data(self, tablename, symbol):
      command_str = "SELECT * FROM %s where symbol = '%s'"%(tablename, symbol)
      return pandas.read_sql_query(sql = command_str, con = self.con, index_col = ['Date'], parse_dates = ['Date'])

   def get_symbols_from_exchange(self, exchange):
      try:
         command_str = "SELECT SYMBOL FROM %s where EXCHANGE = '%s'"%(self.stock_tablename, exchange)
         self.cur.execute(command_str)
         rows = self.cur.fetchall()
         return sorted([n[0].encode() for n in rows])
      except:
         return []
         
if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Pull stock price from Yahoo! Finance and save to SQLite')

   parser.add_argument('-x','--exchange', help='exchange', default = 'SES')

   args = parser.parse_args()
   mds = MarketDataStore("db/mds.sqlite")
   symbols = mds.get_symbols_from_exchange(args.exchange)
   print "============Start pulling market data==============="
   print symbols
   print len(symbols)
   mds.append_hist_data(symbols)
   print "============Finished pulling market data============"
