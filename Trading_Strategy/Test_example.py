import matplotlib.pyplot as plt
import pandas as pd
import tushare as ts

token = '3c311a0c0eb056bfe6c27a161e6cab275649b74245cfd5679a75dca9'
pro = ts.pro_api(token)

all_data = {}
# 遍历list里面的股票，可以写入多个股票
for ticker in ['000011.SZ', '000014.SZ', '000001.SZ', '000002.SZ']:
    # 获取各股票某时段的价格
    all_data[ticker] = pro.daily(ts_code=ticker, start_date='2018-01-01', end_date='2019-01-01')
# 用for循环遍历股票价格并转换为dataframe的形式
price = pd.DataFrame({tic: data['close']
                      for tic, data in all_data.items()})
# 计算股票价格每日变化
ticker_date = pro.daily(ts_code='000011.SZ', start_date='2018-01-01', end_date='2019-01-01')
ticker_date['trade_date'] = pd.to_datetime(ticker_date['trade_date'], format='%Y%m%d')

ticker_date_2 = ticker_date['trade_date']

price['trade_date'] = ticker_date_2

price.set_index('trade_date', inplace=True)

rets = price / price.shift(1) - 1  # shift起平移作用
print(rets.head())

plt.figure(figsize=[18, 5])
price['000011.SZ'].plot()

price_2 = price['000011.SZ']

price_2.rolling(window=20).mean().plot(label='20 day moving average')
price_2.rolling(window=5).mean().plot(label='5 day moving average')
plt.legend(loc='best')

plt.show()
# df_1 = pro.daily(ts_code=stock_list, start_date='20180701', end_date='20180709')


# df_12 = df_1.loc[:, 'open'] ,000002.SZ,000004.SZ,000007.SZ
# returns_1 = df_12.pct_change().dropna()

# sns.jointplot(returns_1, returns_2, kind='reg', height=12)
