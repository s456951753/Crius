import Utils.numeric_utils as TuRq
from datetime import datetime, timedelta
import time as t
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import talib
import Utils.numeric_utils as TuRq

import Utils.configuration_file_service as config_service
import tushare as ts

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)

small_cap_cutoff_up = 1150000  # defind the cutoff for small caps upper end （unit=万元）Note the cutoff is consistent with MSCI small cap definition
small_cap_cutoff_low = 1000000  # defind the cutoff for small caps lower end （unit=万元）
pe_cutoff_up = 5  # defind the cutoff for stock PE ratio
snapshot_date = 20200522

sector_full_list_snapshot = pro.query('daily_basic', ts_code='', trade_date=snapshot_date,fields='ts_code,turnover_rate_f,volume_ratio,pe_ttm,dv_ratio,free_share,total_mv')

list1 = sector_full_list_snapshot[sector_full_list_snapshot['total_mv'].between(small_cap_cutoff_low, small_cap_cutoff_up) & sector_full_list_snapshot['pe_ttm'].between(0.01, pe_cutoff_up)]

print(list1)

list1 = list1['ts_code'].to_list()

stocks = TuRq.get_list_of_converted_stock_code(list1)



print(stocks)

