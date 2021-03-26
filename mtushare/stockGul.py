import tushare as ts
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import mpl_finance as mpf
import datetime
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import queue
from dateutil.relativedelta import relativedelta

updateflag = 0
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


def drawcand(fig,stock,name):
    ax = fig.add_subplot(111)
    # fig.clf()
    # ax = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4, facecolor='#07000d')
    # ax.clear()
    ax.set_xlim(0, len(stock.data_index))
    mpf.candlestick2_ochl(ax, stock.opens, stock.closes, stock.highs, stock.lows, width=0.6, colorup='r', colordown='g')
    # x轴刻度设置
    num = int(len(stock.data_index)/7)
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
    ax.set_title(name)
    x0 = int(len(stock.data_index)*(2/3))
    y0 = stock.opens[len(stock.opens)-x0]
    print(x0)
    print(y0)
    plt.annotate(name, xy=(x0,y0),xytext=(x0,y0-100),
                 arrowprops=dict(arrowstyle='->',facecolor='b'),
                 color='b',fontsize=40)
    return fig


def create_form(figure,root):
    global updateflag
    # 把绘制的图形显示到tkinter窗口上
    print(1)
    canvas = FigureCanvasTkAgg(figure, root)
    print(1)
    # canvas.get_tk_widget().grid(row=2,)
    # canvas._tkcanvas.grid(row=2)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()  # 以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
    updateflag += 1
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


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


def get_code(root,start_time,end_time):
    starttime = start_time
    endtime = end_time
    print(starttime)
    print(endtime)
    # stock_code = codename.get()

    ts.set_token('63253dd8b98756a812fabdb6b2349ac594a5a082ab393910f160459f')
    pro = ts.get_apis()
    days = day(starttime, endtime)
    # 创建绘图对象fig
    fig = plt.figure(figsize=(27, 18))
    canvas = tk.Canvas()  # 创建一块显示图形的画布
    figure = fig
    for codename in stockList:
        print(codename)
        stock_code = codename
        name = stock_code
        df = getDf(stock_code, pro, starttime, endtime)
        stock = stockInfo(days, df)
        figure = drawcand(figure, stock, name)  # 返回matplotlib所画图形的figure对象
    create_form(figure,root)  # 将figure显示在tkinter窗体上面

stockList = list()
q = queue.Queue(maxsize=2)
def updatecode(map,root,start_time,end_time):
    map.destroy()
    map = tk.Toplevel(root)
    map.geometry('1000x600+250+200')
    q.put(map)
    if q.full():
        print(2)
        b = q.get()
        b.destroy()
    get_code(map,start_time,end_time)
    print(q.qsize())
    print(q.full())

def addcode(codename):
    codename = codename.get()
    if codename not in stockList:
        stockList.append(codename)
    for codename in stockList:
        print(codename)
def text(codelist):
    codelist.delete(1.0,tk.END)
    for codename in stockList:
        codelist.insert("end", codename)
        codelist.insert("end", "\n")


def delcode(codename):
    codename = codename.get()
    if codename in stockList:
        stockList.remove(codename)

def month(days,map,root):
    endtime = datetime.datetime.now().strftime('%Y-%m-%d')
    starttime = str(datetime.date.today() - relativedelta(months=+days))
    updatecode(map,root,starttime,endtime)


def manuldays(map,root,start_time,end_time):
    starttime = start_time.get()
    endtime = end_time.get()

    updatecode(map, root, starttime, endtime)


def view():
    root = tk.Tk()
    root.geometry('100x600+128+200')
    map = tk.Toplevel(root)
    map.geometry('1000x600+250+200')
    ADD = tk.Button(root, text='添加股票', width='100',command=lambda : addcode(codename))
    DEL = tk.Button(root, text='删除股票', width='100',command=lambda : delcode(delcodename))
    update = tk.Button(root, text='更新图片',width='100', command=lambda : manuldays(map,root,start_time,end_time))
    amonth = tk.Button(root,text='一个月',width='100',command= lambda : month(1,map,root))
    tmonth = tk.Button(root,text='三个月',width='100',command= lambda : month(3,map,root))
    halfyear = tk.Button(root,text='半年',width='100',command= lambda : month(6,map,root))
    year = tk.Button(root,text='一年',width='100',command= lambda : month(12,map,root))
    textupdate = tk.Button(root,text="获取股票队列",width='100',command= lambda : text(codelist))
    codename = tk.Entry(root)
    delcodename = tk.Entry(root)
    ADD.pack()
    codename.pack()
    DEL.pack()
    delcodename.pack()
    update.pack()
    amonth.pack()
    tmonth.pack()
    halfyear.pack()
    year.pack()
    root.update()
    lb1 = tk.Label(text="开始时间")
    lb1.pack()
    start_time = tk.Entry(root)
    start_time.pack()
    lb2 = tk.Label(text="截至时间")
    lb2.pack()
    end_time = tk.Entry(root)
    end_time.pack()
    lb3 = tk.Label(text="股票队列")
    lb3.pack()
    codelist = tk.Text()
    textupdate.pack()
    codelist.pack()
    root.mainloop()
view()


