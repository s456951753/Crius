# -*- coding: utf-8 -*-


from datetime import date, datetime, timedelta
import time as t
import time
import pandas as pd
import numpy as np
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

#日期格式为 月/日/年
start_date = '4/1/2020'
end_date = '7/1/2020'
start_date_p = '1/1/2020'
end_date_p = '4/1/2020'

#本季度日期范围
datelist = pd.date_range(start=start_date, end=end_date)
date_strings = [datetime.strftime(d, '%Y%m%d') for d in datelist]

#上季度日期范围
datelist_prior = pd.date_range(start=start_date_p, end=end_date_p)
date_strings_prior = [datetime.strftime(d, '%Y%m%d') for d in datelist_prior]

#所有季度基金公司持股文件读取
fund_list = pd.read_excel (r'C:\Users\Austin\Desktop\Tushare\Tushare_Fund_data.xlsx', index = False)

#本季度基金公司持股
fund_list_snapshot = fund_list[fund_list.end_date.isin(date_strings)]

#找出列表中重复披露的行,取更旧的日期
drop_list0 = fund_list_snapshot.copy()
drop_list1 = drop_list0[:, 'ts_code', 'end_date']


drop_list1['size'] = drop_list1.groupby(['ts_code', 'end_date']).count()

print(drop_list1)
