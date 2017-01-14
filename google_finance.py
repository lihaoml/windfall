import urllib,time,datetime
import urllib
from urllib2 import urlopen
from bs4 import BeautifulSoup
import requests
from datetime import datetime,date,timedelta
import pandas as pd
import time

def google_hist_price(symbol_input, start_date, end_date=date.today().isoformat()):
  symbol_to_query = symbol_input.upper().split(".")[0]
  df = pd.DataFrame()
  start = date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
  end = date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
  date_list = []
  delta = 200 # the maximum row google's historical data page can display
  intervals = (end - start).days / delta
  for i in range(0, intervals + 1):
    date_list.append( ( start+i*timedelta(delta), min(end, start+(i+1)*timedelta(delta)-timedelta(1)) )  )
  
  for (d1, d2) in date_list:
    url_string = "http://www.google.com/finance/historical?q={0}".format(symbol_to_query)
    url_string += "&num=200&startdate={0}&enddate={1}".format(d1.strftime('%b %d, %Y'), d2.strftime('%b %d, %Y'))
    print url_string
    time.sleep(1)
    page2 = urllib.urlopen(url_string).read()
    soup = BeautifulSoup(page2, "lxml")
    
    headers = [h.string.rstrip().encode() for h in soup.findAll("th")]
    dct = {key: [] for key in headers}

    if (not(any(dct))):
      continue

    for row in soup.find_all('tr')[5:]:
      tds = [d.string.rstrip().encode() for d in row.find_all('td')]
      for (h, d) in zip(headers, tds):
        dct[h].append(d)

    def safeConvert(f, x):
      try:
        return f(x)
      except:
        return f('nan')
    
    dct['Date'] = [datetime.strptime(d, "%b %d, %Y").date().strftime("%Y-%m-%d") for d in dct['Date']]
    dct['Volume'] = [safeConvert(int, d.replace(",", "")) for d in dct['Volume']]
    dct['Open'] = [safeConvert(float, d.replace(",", "")) for d in dct['Open']]
    dct['Close'] = [safeConvert(float, d.replace(",", "")) for d in dct['Close']]
    dct['High'] = [safeConvert(float, d.replace(",", "")) for d in dct['High']]
    dct['Low'] = [safeConvert(float, d.replace(",", "")) for d in dct['Low']]
      
    if df.empty:
      df = pd.DataFrame(dct)
    else:
      df = df.append(pd.DataFrame(dct))

  if not(df.empty):
    df['Symbol'] = symbol_input
    df = df.set_index(['Symbol', 'Date'], drop=True, append=False, verify_integrity = True).sort_index()
  return df
    
def google_hist_price_csv(symbol,start_date,end_date=date.today().isoformat()):
  ''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
  symbol = symbol.upper()
  start = datetime.date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
  end = datetime.date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
  url_string = "http://www.google.com/finance/historical?q={0}".format(symbol)
  url_string += "&output=csv&startdate={0}&enddate={1}".format(
    start.strftime('%b %d, %Y'),end.strftime('%b %d, %Y'))
  
  print url_string
  csv = urllib.urlopen(url_string).readlines()
  soup = BeautifulSoup(csv, 'html.parser')
  print soup
  print csv
 
if __name__ == '__main__':
  q = google_hist_price('BN4','2016-01-01')            # download year to date Apple data
  print q                                           # print it out
  # q = GoogleQuote('orcl','2011-11-01','2011-11-30') # download Oracle data for February 2011
  # print q


