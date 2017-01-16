import dbutils
import pandas as pd

mds = dbutils.MarketDataStore('db/mds.sqlite')

symbol = 'BN4.SI'

yahoo_data = mds.get_hist_data(mds.hist_data_yahoo_tablename, symbol);
google_data = mds.get_hist_data(mds.hist_data_google_tablename, symbol);


yData = yahoo_data.drop('Symbol', axis=1).add_prefix('Y_')
gData = google_data.drop('Symbol', axis=1).add_prefix('G_')

print pd.concat([yData, gData], axis=1)
