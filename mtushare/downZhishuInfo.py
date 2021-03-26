import tushare as ts
from sqlalchemy import create_engine
from pymysql import *
from queue import Queue
import threading
import datetime
ts.set_token('63253dd8b98756a812fabdb6b2349ac594a5a082ab393910f160459f')
pro = ts.get_apis()
# 获取ts_code,并放入队列
stock_code_queue = Queue()
# 医药主题：000121 国证军工：399368 公共健康:399277 有色金属：000819
# it指数：399239 采矿指数：399232 金融指数：399240 地产指数：399241
# 科创50： 000688 优势能源：000145
datas = ['000121', '399368', '399277', '000819',
         '399239', '399232', '399240', '399241',
         '000688', '000145']
for i in datas:
    stock_code_queue.put(i)

# 从队列里获取每只股票的复权信息
def get_stock_info(stock_code_queue,pro):
    global count
    endtime = datetime.datetime.now().strftime('%Y-%m-%d')
    while stock_code_queue.qsize()!=0:
        code = stock_code_queue.get()
        try:
            dfz = ts.bar(code, conn=pro, asset='INDEX', start_date='20010101', end_date=endtime)
            # df = ts.pro_bar(ts_code=code, adj='qfq',start_date='20010101',end_date=endtime)
            print("正在获取%s;数据还有%s条:" % (code, stock_code_queue.qsize()))
            res = dfz.to_csv('./info/%s.cvs' % code)
        # except AttributeError:
        #     print("a")
        #     pass
        except Exception as ret:
            print(ret)
            stock_code_queue.put(code)

get_stock_info(stock_code_queue,pro)
# qf = threading.Thread(target=get_stock_info,args=(stock_code_queue,))
# qf.start()
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