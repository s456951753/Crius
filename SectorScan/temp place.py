from datetime import datetime, timedelta

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import tushare as ts
token='3c311a0c0eb056bfe6c27a161e6cab275649b74245cfd5679a75dca9'
pro=ts.pro_api(token)

snapshot_date = '20200507'

list_days_filter = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,list_date')
list_days_filter['list_date'] = pd.to_datetime(list_days_filter['list_date'],format='%Y%m%d')
list_days_filter['snapshot_date'] = snapshot_date
list_days_filter['snapshot_date'] = pd.to_datetime(list_days_filter['snapshot_date'],format='%Y%m%d')
list_days_filter['list_days'] = (list_days_filter['snapshot_date'] - list_days_filter['list_date']).dt.days
list_days_filter2 = list_days_filter[list_days_filter['list_days'] > 730]

list_days_filter_list = list_days_filter2['ts_code'].tolist()


#Export the df to excel
#list_days_filter.to_excel(r'C:\Users\Austin\Desktop\Tushare\list3.xlsx', index = False)

print(list_days_filter_list)

#df1['snapshot_date'] = datetime.strptime(snapshot_date, '%Y%m%d').date()