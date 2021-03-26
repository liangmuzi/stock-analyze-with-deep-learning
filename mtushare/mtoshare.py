import tushare as ts
from sqlalchemy import create_engine
from pymysql import *
from queue import Queue
import threading

ts.set_token('63253dd8b98756a812fabdb6b2349ac594a5a082ab393910f160459f')
pro = ts.pro_api('63253dd8b98756a812fabdb6b2349ac594a5a082ab393910f160459f')
conn =create_engine('mysql+pymysql://root:toor@localhost/tushare_data',encoding='utf8')
# 获取ts_code,并放入队列
datas = pro.stock_basic()
stock_code_queue = Queue()
for i in datas.index:
    data = datas.at[i, "ts_code"]
    stock_code_queue.put(data)

# 从队列里获取每只股票的复权信息
def get_stock_info(stock_code_queue):
    global count
    while stock_code_queue.qsize()!=0:
        code = stock_code_queue.get()
        try:
            df = ts.pro_bar(ts_code=code, adj='qfq',start_date='20010101',end_date='20210203')
            print("正在获取%s;数据还有%s条:" % (code, stock_code_queue.qsize()))
            res = df.to_sql('stock_basic', conn, index=False, if_exists='append', chunksize=5000)
        except AttributeError:
            print("a")
            pass
        except:
            stock_code_queue.put(code)


q1 = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
q1.start()
q2 = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
q2.start()
q3 = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
q3.start()
q4 = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
q4.start()
q5 = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
q5.start()
q6 = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
q6.start()
q7 = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
q7.start()
q8 = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
q8.start()
q9 = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
q9.start()
qa = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
qa.start()
qc = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
qc.start()
qd = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
qd.start()
qe = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
qe.start()
qf = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
qf.start()
"""
| stock_basic | CREATE TABLE `stock_basic` (
  `ts_code` text,
  `symbol` text,
  `name` text,
  `area` text,
  `industry` text,
  `market` text,
  `list_date` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8 |
  ts_code trade_date   open   high  ...  change  pct_chg        vol       amount
0  000002.SZ   20210203  28.34  28.35  ...   -0.42   -1.482  589610.04  1646692.738

"""
#获取对应的股票复权信息
#将股票复权信息入库