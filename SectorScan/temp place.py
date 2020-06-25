# -*- coding: utf-8 -*-


from datetime import date, datetime, timedelta
import time as t
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import talib

from multiprocessing.dummy import Pool as ThreadPool

#Load Tushare
from rqalpha.apis.api_base import history_bars, get_position
from rqalpha.mod.rqalpha_mod_sys_accounts.api.api_stock import order_target_value, order_value

import Utils.configuration_file_service as config_service
import tushare as ts

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)


#公募基金持仓数据
list = pro.fund_basic(market='E')
list = list['ts_code'].to_list()

pool = ThreadPool()
appended_data = pool.map(pro.fund_portfolio, list)
pool.close()
pool.join()

appended_data = []
for fund_code in list:
    all_data = pro.fund_portfolio(ts_code=fund_code)
    appended_data.append(all_data)

appended_data = pd.concat(appended_data)

#Export the df to excel
appended_data.to_excel(r'C:\Users\Austin\Desktop\Tushare\list3.xlsx', index = False)

