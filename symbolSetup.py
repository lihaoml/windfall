import pandas as pd
import sqlite3 as lite

def googleSymbol (row):
    return row['Google Symbol'].split('.')[0]

df = pd.DataFrame.from_csv('db/yahooSymbols.csv')
# print df
# save to database

df['Google Symbol'] = df.index
df['Google Symbol'] = df.apply(googleSymbol, axis = 1)

print df

con = lite.connect('db/mds.sqlite')
con.text_factory = str

df.to_sql('STOCK', con, if_exists = 'replace', index = True, index_label=['Symbol'])


#con.close()



