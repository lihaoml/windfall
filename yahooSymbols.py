import pandas as pd
import sqlite3 as lite

df = pd.DataFrame.from_csv('db/yahooSymbols.csv')
print df
# save to database

con = lite.connect('db/mds.sqlite')
con.text_factory = str

df.to_sql('STOCK', con, if_exists = 'replace', index = True, index_label=['Symbol'])


con.close()



