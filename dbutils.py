#!/usr/local/bin/python

from yahoo_finance import Share

import argparse
import datetime, time

import sqlite3 as lite
import pandas

class MarketDataStore:
   """ Storing and retrieving market data from database (SQLite)

   """
   def __init__(self, db_path):
      self.con = lite.connect(db_path)
      self.cur = self.con.cursor()
      self.hist_data_tablename = 'HIST_DATA'
      self.stock_tablename = 'STOCK'

   def __del__(self):
      self.con.close()

   def append_hist_data(self, stock_sym_list):
      """       
      """
      today = datetime.date.today()
      for symbol in stock_sym_list:
         print ("pulling " + symbol)
         stock = Share(symbol)
         last_date = self.get_last_date(symbol)
         # filter out the strings in the returned list
         ts_ = [t for t in stock.get_historical(last_date.strftime("%Y-%m-%d"),today.strftime("%Y-%m-%d")) if type(t) != type("")]
         ts = [t for t in ts_ if t['Date'] == t['Date']] # check that date is not nan
         # when there is no data to retrieve, get_historical returns a list of strings where each string is the column name
         # when there is data, get_historical returns a list of dict
         if len(ts) > 0:
            df = pandas.DataFrame(ts).set_index(['Symbol', 'Date'], drop=True, append=False, verify_integrity = True)
            print df
            df.to_sql(self.hist_data_tablename, self.con, schema=None, if_exists='append', index=True, index_label=['Symbol', 'Date'])
         else:
            print "%s: no new data to be added from %s to %s"%(symbol, last_date, today)
         
   def get_last_date(self, symbol):
      try:
         command_str = "SELECT DATE FROM %s where symbol = '%s'"%(self.hist_data_tablename, symbol)
         self.cur.execute(command_str)
         rows = self.cur.fetchall()
         return datetime.datetime.strptime(max([n[0].encode() for n in rows]), "%Y-%m-%d").date()
      except:
         return datetime.date(1990, 1, 1)

   def get_hist_data(self, symbol):
      command_str = "SELECT * FROM %s where symbol = '%s'"%(self.hist_data_tablename, symbol)
      return pandas.read_sql_query(sql = command_str, con = self.con, index_col = ['Date'], parse_dates = ['Date'])

   def get_symbols_from_exchange(self, table, exchange):
      try:
         command_str = "SELECT SYMBOL FROM %s where EXCHANGE = '%s'"%(table, exchange)
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
   symbols = mds.get_symbols_from_exchange(mds.stock_tablename, args.exchange)
   print "============Start pulling market data==============="
   print symbols
   print len(symbols)
   mds.append_hist_data(symbols)
   print "============Finished pulling market data============"
