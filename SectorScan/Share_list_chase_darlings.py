import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import tushare as ts
token='3c311a0c0eb056bfe6c27a161e6cab275649b74245cfd5679a75dca9'
pro=ts.pro_api(token)

#Setup

full_list = pro.fund_basic(market='E') #TODO: use formula to remove '增强指数型' and '被动指数型' under 'invest_type'

temp_list1 = pro.fund_nav(ts_code=full_list) #TODO: use formula to filter 'net_asset' to select top 50.

temp_list2 = pro.fund_portfolio(ts_code=temp_list1) #获取公募基金持仓数据，季度更新

#TODO: perform temp_list2 for current quarter and the Q-1. Compare the stock list and identify 'addition' and 'deletion'

print(df)

#Export the df to excel
df.to_excel(r'C:\Users\Austin\Desktop\Tushare\list3.xlsx', index = False)


df = pro.fund_nav(ts_code='165509.SZ')