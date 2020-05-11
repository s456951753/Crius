from datetime import datetime, timedelta

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import tushare as ts
token='3c311a0c0eb056bfe6c27a161e6cab275649b74245cfd5679a75dca9'
pro=ts.pro_api(token)

snapshot_date = '20200507'

list = ['000685.SZ', '000690.SZ', '000935.SZ', '000937.SZ', '002004.SZ', '002048.SZ',
        '002419.SZ', '002430.SZ', '002440.SZ', '002444.SZ', '002531.SZ', '002597.SZ',
        '002605.SZ', '002798.SZ', '300080.SZ', '300118.SZ', '600064.SH', '600295.SH', '600329.SH',
        '600348.SH', '600507.SH', '600682.SH', '600717.SH', '600729.SH', '600803.SH', '601107.SH',
        '601163.SH', '601330.SH', '601567.SH', '603328.SH']

#get multi-year key financial info then covert to dataframe
fina_start_date = 20170930 #TODO: this part to be automated later, reference snapshot_date
fina_end_date = 20191231 #TODO: this part to be automated later reference snapshot_date

fin_data = {}
for ticker in list:
    fin_data = pro.query('fina_indicator_vip', ts_code=ticker, start_date=fina_start_date, end_date=fina_end_date, fields='ts_code,end_date,debt_to_eqt,roe_avg,gross_margin,ebt_yoy')

fin_data_list = pd.DataFrame({fin_data})


#Export the df to excel
#list_days_filter.to_excel(r'C:\Users\Austin\Desktop\Tushare\list3.xlsx', index = False)

print(fin_data)

#df1['snapshot_date'] = datetime.strptime(snapshot_date, '%Y%m%d').date()