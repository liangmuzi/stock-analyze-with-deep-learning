import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
data = pd.read_csv('./info/000121.csv')
data.datetime = pd.to_datetime(data['datetime'])
x = data.datetime[3]
data = data.set_index('datetime',drop=False)
df = data['2021-03-10':'2021-03-08']
print(df)
plt.figure(figsize=(10,5))#设置画布的尺寸
plt.title('Examples of line chart',fontsize=20)#标题，并设定字号大小
plt.xlabel(u'x-year',fontsize=14)#设置x轴，并设定字号大小
plt.ylabel(u'y-income',fontsize=14)#设置y轴，并设定字号大小
df = df.reset_index(drop=True)
print(df)
plt.plot(df['datetime'],df['close'],color="deeppink",linewidth=2,linestyle=':',label='Jay income', marker='+')
plt.show()
# ts.set_token('63253dd8b98756a812fabdb6b2349ac594a5a082ab393910f160459f')
# pro = ts.get_apis()
# print(dfz)
'''              code    open   close  ...      vol       amount  p_change
datetime                            ...                                
2005-12-30  000121  797.15  792.20  ...  10227.0  651430144.0     -0.06
2005-12-29  000121  784.47  792.64  ...   9954.0  573668352.0      1.36
2005-12-28  000121  783.27  782.00  ...   5094.0  290403392.0     -0.05
2005-12-27  000121  781.48  782.38  ...   5012.0  268001360.0      0.09
2005-12-26  000121  777.76  781.67  ...   6304.0  360519808.0      0.49
'''
'''        datetime  code       open  ...      vol        amount  p_change
0     2021-03-10   121  11673.626  ...  40663.0  1.904016e+10      0.71
1     2021-03-09   121  11813.017  ...  56407.0  2.411569e+10     -2.52
2     2021-03-08   121  12257.017  ...  55982.0  2.445372e+10     -3.03
3     2021-03-05   121  12010.276  ...  44433.0  1.909848e+10      0.64
4     2021-03-04   121  12380.536  ...  49433.0  2.145189e+10     -2.61
...'''
'''     datetime    code       open  ...      vol        amount  p_change
58 2020-12-15  000121  12577.700  ...  58001.0  2.774584e+10       NaN
57 2020-12-16  000121  12710.420  ...  51556.0  2.250739e+10     -0.05
56 2020-12-17  000121  12742.500  ...  67388.0  3.268062e+10      1.17
'''