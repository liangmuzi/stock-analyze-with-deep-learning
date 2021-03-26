import tushare as ts
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import mpl_finance as mpf
import datetime
import time


def day(starttime,endtime):
    timeArray = time.strptime(starttime, "%Y-%m-%d")
    starttime = datetime.date(timeArray.tm_year,timeArray.tm_mon,timeArray.tm_mday)
    timeArray1 = time.strptime(endtime,"%Y-%m-%d")
    endtime = datetime.date(timeArray1.tm_year,timeArray1.tm_mon,timeArray1.tm_mday)
    return endtime.__sub__(starttime).days


def getDf(stock_code,pro,starttime, endtime):
    #dfz = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date='20010101', end_date='20210203')
    dfz = ts.bar(stock_code, conn=pro, asset='INDEX', start_date=starttime, end_date=endtime)
    dfz = dfz.reset_index()
    df = dfz.reindex(index=dfz.index[::-1])
    print(df)
    return df


def drawcand(stock,stock1):
    # 设置x轴的范围
    fig = plt.figure(figsize=(27, 18))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, len(stock1.data_index))
    mpf.candlestick2_ochl(ax, stock.opens, stock.closes, stock.highs, stock.lows, width=0.6, colorup='r', colordown='g')
    mpf.candlestick2_ochl(ax, stock1.opens, stock1.closes, stock1.highs, stock1.lows, width=0.6, colorup='r', colordown='g')
    # x轴刻度设置
    num = int(len(stock.data_index)/10)
    ax.set_xticks(np.arange(0, len(stock.data_index), num))
    print(len(stock.data_index))
    # 标签设置为日期
    print(stock.data_index)
    print(stock.data_index[0])

    print(ax.get_xticks())
    ax.set_xticklabels([stock.data_index[index] for index in ax.get_xticks()])
    # 设置轴标签
    ax.set_xlabel('Date', fontsize=15)
    ax.set_ylabel('Price', fontsize=15)
    ax.set_title(stock_code)
    x0 = int(len(stock.data_index)*(2/3))
    y0 = stock.opens[len(stock.opens)-x0]
    y1 = stock1.opens[len(stock1.opens)-x0]
    print(x0)
    print(y0)
    print(y1)
    plt.annotate('hushen300', xy=(x0,y0),xytext=(x0,y0-100),
                 arrowprops=dict(arrowstyle='->',facecolor='b'),
                 color='b',fontsize=40)
    plt.annotate('shangzheng50', xy=(x0,y1),xytext=(x0,y1-50),
                 arrowprops=dict(arrowstyle='->',facecolor='b'),
                 color='b',fontsize=40)
    plt.savefig('./image/1%s.png' % stock_code)
    plt.show()


class stockInfo:
    def __init__(self,days,df):
        self.opens = df['open'][0:days]
        #print(opens)
        self.closes = df['close'][0:days]
        self.highs = df['high'][0:days]
        self.lows = df['low'][0:days]
        #去掉分钟精度
        self.data_index = df['datetime'][0:days].dt.date
        # 设置新索引
        self.data_index = self.data_index.reset_index(drop=True)


ts.set_token('63253dd8b98756a812fabdb6b2349ac594a5a082ab393910f160459f')
pro = ts.get_apis()
starttime = '2020-1-1'
endtime = '2021-2-22'
days = day(starttime, endtime)
stock_code = '000300'
stock_code1 = '000016'
df = getDf(stock_code, pro, starttime, endtime)
df1 = getDf(stock_code1, pro, starttime, endtime)
#df1 = getDf(stock_code1,pro)
#df2 = getDf(stock_code2,pro)
stock = stockInfo(days,df)
stock1 = stockInfo(days,df1)
drawcand(stock,stock1)
#stock2 = stockInfo(days,df1)
#stock3 = stockInfo(days,df2)
#ohlc = list(zip(np.arange(0,len(stock1.opens)),stock1.opens,stock1.closes,stock1.highs,stock1.lows))
#mpf.candlestick2_ochl(ax, stock3.opens, stock3.closes, stock3.highs, stock3.lows, width=0.6, colorup='r', colordown='g')

