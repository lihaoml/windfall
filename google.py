# Copyright (c) 2011, Mark Chenoweth
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted 
# provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following 
#   disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS 
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import urllib,time,datetime
import urllib
from urllib2 import urlopen
from bs4 import BeautifulSoup
import requests
from datetime import datetime,date,timedelta
import pandas as pd


class GoogleQuoteGeneral():
  def __init__(self, symbol,start_date, end_date=date.today().isoformat()):
    self.symbol = symbol.upper()

    df = pd.DataFrame()
    
    start = date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
    end = date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
    date_list = []
    delta = 200 # the maximum row google's historical data page can display
    intervals = (end - start).days / delta
    for i in range(0, intervals + 1):
      date_list.append( ( start+i*timedelta(delta), min(end, start+(i+1)*timedelta(delta)-timedelta(1)) )  )

    for (d1, d2) in date_list:
      url_string = "http://www.google.com/finance/historical?q={0}".format(self.symbol)
      url_string += "&num=200&startdate={0}&enddate={1}".format(d1.strftime('%b %d, %Y'), d2.strftime('%b %d, %Y'))
      print url_string

      page2 = urllib.urlopen(url_string).read()
      soup = BeautifulSoup(page2, "lxml")
    
      headers = [h.string.rstrip().encode() for h in soup.findAll("th")]
      dct = {key: [] for key in headers}
      for row in soup.find_all('tr')[5:]:
        tds = [d.string.rstrip().encode() for d in row.find_all('td')]
        for (h, d) in zip(headers, tds):
          dct[h].append(d)
        
      dct['Date'] = [datetime.strptime(d, "%b %d, %Y").date() for d in dct['Date']]
      dct['Volume'] = [int(d.replace(",", "")) for d in dct['Volume']]
      dct['Open'] = [float(d.replace(",", "")) for d in dct['Open']]
      dct['Close'] = [float(d.replace(",", "")) for d in dct['Close']]
      dct['High'] = [float(d.replace(",", "")) for d in dct['High']]
      dct['Low'] = [float(d.replace(",", "")) for d in dct['Low']]

      if df.empty:
        df = pd.DataFrame(dct).set_index('Date')
      else:
        df = df.append(pd.DataFrame(dct).set_index('Date'))
      
    print df
    
   
class GoogleQuote():
  ''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
  def __init__(self,symbol,start_date,end_date=date.today().isoformat()):
    self.symbol = symbol.upper()
    start = datetime.date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
    end = datetime.date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
    url_string = "http://www.google.com/finance/historical?q={0}".format(self.symbol)
    url_string += "&output=csv&startdate={0}&enddate={1}".format(
                      start.strftime('%b %d, %Y'),end.strftime('%b %d, %Y'))

    print url_string
    csv = urllib.urlopen(url_string).readlines()
    soup = BeautifulSoup(csv, 'html.parser')
    print soup
    print csv
 
if __name__ == '__main__':
  q = GoogleQuoteGeneral('BN4','2016-01-01')            # download year to date Apple data
  print q                                           # print it out
  # q = GoogleQuote('orcl','2011-11-01','2011-11-30') # download Oracle data for February 2011
  # print q


