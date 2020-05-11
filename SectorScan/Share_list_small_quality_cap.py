# -*- coding: utf-8 -*-


from rqalpha import run_code


from datetime import datetime, timedelta
import time as t
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import talib

#Load Tushare
from rqalpha.apis.api_base import history_bars, get_position
from rqalpha.mod.rqalpha_mod_sys_accounts.api.api_stock import order_target_value, order_value

import Utils.configuration_file_service as config_service
import tushare as ts

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)

# Load rqalpha
from rqalpha.api import *

#Setup - fundamental section
snapshot_date = '20200507'
small_cap_cutoff_up = 1150000 #defind the cutoff for small caps upper end （unit=万元）Note the cutoff is consistent with MSCI small cap definition
small_cap_cutoff_low = 1050000 #defind the cutoff for small caps lower end （unit=万元）
pe_cutoff_up = 30 #defind the cutoff for stock PE ratio

#Setup - technical section...


#Extract basic stock information
#sector_full_list = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,is_hs')


#Extract basic stock information - company introduction
#sector_full_list_intro = pro.stock_company(exchange='SZSE', fields='ts_code,chairman,manager,secretary,website,introduction,main_business')

#get daily metrics
sector_full_list_snapshot = pro.query('daily_basic', ts_code='', trade_date=snapshot_date,
                                      fields='ts_code,turnover_rate_f,volume_ratio,pe_ttm,dv_ratio,free_share,total_mv')

#Select small cap stocks with pre-defined cutoffs and with pre-defined PE range
templist1 = sector_full_list_snapshot[sector_full_list_snapshot['total_mv'].between(small_cap_cutoff_low, small_cap_cutoff_up) & sector_full_list_snapshot['pe_ttm'].between(0.01, pe_cutoff_up)]


#remove stocks that had up limited in the last x days
up_start_date = 20200424 #TODO: this part to be automated later, reference snapshot_date
up_end_date = 20200507 #TODO: this part to be automated later reference snapshot_date

up_list = pro.limit_list(start_date=up_start_date, end_date=up_end_date)['ts_code']

templist2 = templist1[~templist1.ts_code.isin(up_list)]
t.sleep(1)

#filter on stocks with at least three years trading history #TODO: the three year variable shoudl be an input field
list_days_filter = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,list_date')
list_days_filter['list_date'] = pd.to_datetime(list_days_filter['list_date'],format='%Y%m%d')
list_days_filter['snapshot_date'] = snapshot_date
list_days_filter['snapshot_date'] = pd.to_datetime(list_days_filter['snapshot_date'],format='%Y%m%d')
list_days_filter['list_days'] = (list_days_filter['snapshot_date'] - list_days_filter['list_date']).dt.days
list_days_filter2 = list_days_filter[list_days_filter['list_days'] > 730]

templist3 = templist2[~templist2.ts_code.isin(list_days_filter2)]

templist4 =templist3['ts_code'].tolist()

#print(templist4)

#get multi-year key financial info then covert to dataframe
fina_start_date = 20170930 #TODO: this part to be automated later, reference snapshot_date
fina_end_date = 20191231 #TODO: this part to be automated later reference snapshot_date

fin_data = {} #TODO: Not working yet
for ticker in templist4:
    fin_data = pro.query('fina_indicator_vip', ts_code=ticker, start_date=fina_start_date, end_date=fina_end_date,
                         fields='ts_code,end_date,debt_to_eqt,roe_avg,gross_margin,ebt_yoy')

fin_data_list = pd.DataFrame({stockitem: data['ts_code,end_date,debt_to_eqt,roe_avg,gross_margin,ebt_yoy']
                    for stockitem, data in fin_data.items()})
#TODO: the above section is not working yet




#Export the df to excel
#fin_data.to_excel(r'C:\Users\Austin\Desktop\Tushare\list2.xlsx', index = False)
