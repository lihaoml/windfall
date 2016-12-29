import urllib2
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
import matplotlib
import pylab
matplotlib.rcParams.update({'font.size': 9})

def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)
    
    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter
        
        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
            
        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n
            
        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)
            
    return rsi
        
def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array

def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def computeMACD(x, slow=26, fast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow


def graphData(stock,MA1,MA2):
    try:
        stockFile ="db/" + stock + ".txt"
        date, openp, highp, lowp, closep, volume = np.loadtxt(stockFile,delimiter=',', unpack=True, converters={ 0: mdates.strpdate2num('%Y-%m-%d')})
        x = 0
        y = len(date)
        newAr = []
        while x < y:
            appendLine = date[x],openp[x],closep[x],highp[x],lowp[x],volume[x]
            newAr.append(appendLine)
            x+=1
            
        Av1 = movingaverage(closep, MA1)
        Av2 = movingaverage(closep, MA2)
            
        SP = len(date[MA2-1:])
            
            
        ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4)
        candlestick_ohlc(ax1, newAr[-SP:], width=.6)
            
        Label1 = str(MA1)+' SMA'
        Label2 = str(MA2)+' SMA'
            
        ax1.plot(date[-SP:],Av1[-SP:],'#e1edf9',label=Label1, linewidth=1.5)
        ax1.plot(date[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
            
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        plt.ylabel('Stock price and Volume')
                    
        maLeg = plt.legend(loc=9, ncol=2, prop={'size':7},
                           fancybox=True, borderaxespad=0.)
        maLeg.get_frame().set_alpha(0.4)
        textEd = pylab.gca().get_legend().get_texts()
#        pylab.setp(textEd[0:5], color = 'w')
        
        volumeMin = 0
        
        ax0 = plt.subplot2grid((6,4), (0,0), sharex=ax1, rowspan=1, colspan=4)
        rsi = rsiFunc(closep)
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        
        ax0.plot(date[-SP:], rsi[-SP:], rsiCol, linewidth=1.5)
        ax0.axhline(70, color=negCol)
        ax0.axhline(30, color=posCol)
        ax0.fill_between(date[-SP:], rsi[-SP:], 70, where=(rsi[-SP:]>=70), facecolor=negCol, edgecolor=negCol, alpha=0.5)
        ax0.fill_between(date[-SP:], rsi[-SP:], 30, where=(rsi[-SP:]<=30), facecolor=posCol, edgecolor=posCol, alpha=0.5)
        ax0.set_yticks([30,70])
        plt.ylabel('RSI')
            
        ax1v = ax1.twinx()
        ax1v.fill_between(date[-SP:],volumeMin, volume[-SP:], alpha=.4)
        ax1v.axes.yaxis.set_ticklabels([])
        ax1v.grid(False)
        ax1v.set_ylim(0, 3*volume.max())
            
        ax2 = plt.subplot2grid((6,4), (5,0), sharex=ax1, rowspan=1, colspan=4)
            
                    
            
        # START NEW INDICATOR CODE #
            
                    
            
        # END NEW INDICATOR CODE #
                    
                    
                
                    
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))
            
        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)
                
        plt.suptitle(stock.upper())
            
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)
                
        plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
        plt.show()
                
    except Exception,e:
        print 'main loop',str(e)
                
stock = raw_input('Stock to plot: ')
graphData(stock,10,50)
