import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import tushare as ts
token='3c311a0c0eb056bfe6c27a161e6cab275649b74245cfd5679a75dca9'
pro=ts.pro_api(token)

snapshot_date = 20200507

stocks1 = pro.query('stock_basic', ts_code='600634.SH，000835.SZ', trade_date=snapshot_date,fields='ts_code,list_date')

print(stocks1)


ticker_list = stocks1['ts_code'].to_list()

for ticker in ticker_list:
    days_public=pd.to_datetime(snapshot_date,format='%Y%m%d') - pd.to_datetime(stocks1['list_date'],format='%Y%m%d')
if days_public<30:
    stocks1.remove(ticker)

