# -*- coding: utf-8 -*-


from datetime import date, datetime, timedelta
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

import Utils.numeric_utils as TuRq

list1 = ['601360.XSHG']

list2 = TuRq.get_list_of_converted_stock_code(list1)

print(list2)



#Export the df to excel
#up_list.to_excel(r'C:\Users\Austin\Desktop\Tushare\list4.xlsx', index = False)
