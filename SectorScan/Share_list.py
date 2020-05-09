import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import tushare as ts
token='3c311a0c0eb056bfe6c27a161e6cab275649b74245cfd5679a75dca9'
pro=ts.pro_api(token)

#Setup - fundamental section
snapshot_date = 20200507
small_cap_cutoff_up = 1150000 #defind the cutoff for small caps upper end （unit=万元）Note the cutoff is consistent with MSCI small cap definition
small_cap_cutoff_low = 0 #defind the cutoff for small caps lower end （unit=万元）
pe_cutoff_up = 30 #defind the cutoff for stock PE ratio

#Setup - technical section

#Extract basic stock information
#sector_full_list = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,is_hs')

#Extract basic stock information - company introduciton
#sector_full_list_intro = pro.stock_company(exchange='SZSE', fields='ts_code,chairman,manager,secretary,website,introduction,main_business')

#Extract basic stock information - trading snapshot
sector_full_list_snapshot = pro.query('daily_basic', ts_code='', trade_date=snapshot_date,fields='ts_code,turnover_rate_f,volume_ratio,pe_ttm,dv_ratio,free_share,total_mv')

templist1 = sector_full_list_snapshot[sector_full_list_snapshot['total_mv'].between(small_cap_cutoff_low, small_cap_cutoff_up) & sector_full_list_snapshot['pe_ttm'].between(0.01, pe_cutoff_up)]
#select small cap stocks with pre-defined cutoffs and with pre-defined PE range

#templist2 = templist1[templist1['pe_ttm'].between(0.01, pe_cutoff_up)] #select stocks with pre-defined PE range


#sector_full_list_snapshot.sort_values(by='total_mv')


#Strategy one
#Look for mid to small cap, reasonable PE, no up limited in the last 30 days, reasonable gearing,

print(templist1)

#Export the df to excel
templist1.to_excel(r'C:\Users\Austin\Desktop\Tushare\list2.xlsx', index = False)
