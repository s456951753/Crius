# -*- coding: utf-8 -*-


from datetime import date, datetime, timedelta
import time as t
import time
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

import Utils.numeric_utils as TuRq

#df2 = pro.index_classify(level='L2', src='SW')


#Express data

list = pro.fund_basic(market='E')
list = list['ts_code'].to_list()

appended_data = []
for fund_code in list:
    all_data = pro.fund_portfolio(ts_code=fund_code)
    appended_data.append(all_data)
appended_data = pd.concat(appended_data)

#Export the df to excel
all_data.to_excel(r'C:\Users\Austin\Desktop\Tushare\list3.xlsx', index = False)

