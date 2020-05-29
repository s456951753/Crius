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

#新建一个column使得每个row的数据都是唯一的。第一步把end_date 改成string 格式
fund_list_snapshot['end_date2'] = fund_list_snapshot['end_date'].apply(str)
fund_list_snapshot['uniquecode1'] = fund_list_snapshot.ts_code + "_" + fund_list_snapshot.end_date2
fund_list_snapshot['uniquecode2'] = fund_list_snapshot.ts_code + "_" + fund_list_snapshot.symbol + "_" + fund_list_snapshot.end_date2

#找出列表中重复披露的行,取更旧的日期
drop_list = fund_list_snapshot.sort_values('end_date').drop_duplicates(subset=['ts_code'], keep='first')
drop_list = drop_list['uniquecode1'].to_list()

#剔除列表中重复披露的行
fund_list_snapshot = fund_list_snapshot[~fund_list_snapshot['uniquecode1'].isin(drop_list)]

#最终列表整理
fund_list_snapshot2 = pd.pivot_table(fund_list_snapshot,index=["symbol"],aggfunc={'stk_mkv_ratio':np.sum,'ts_code':np.count_nonzero,'mkv':np.sum,'amount':np.sum})
fund_list_snapshot2 = fund_list_snapshot2.sort_values(by='stk_mkv_ratio', ascending=False)

#上季度基金公司持股
fund_list_snapshot_prior = fund_list[fund_list.end_date.isin(date_strings_prior)]

#新建一个column使得每个row的数据都是唯一的。第一步把end_date 改成string 格式
fund_list_snapshot_prior['end_date2'] = fund_list_snapshot_prior['end_date'].apply(str)
fund_list_snapshot_prior['uniquecode1'] = fund_list_snapshot_prior.ts_code + "_" + fund_list_snapshot_prior.end_date2
fund_list_snapshot_prior['uniquecode2'] = fund_list_snapshot_prior.ts_code + "_" + fund_list_snapshot_prior.symbol + "_" + fund_list_snapshot_prior.end_date2

#找出列表中重复披露的行,取更旧的日期
drop_list = fund_list_snapshot_prior.sort_values('end_date').drop_duplicates(subset=['ts_code'], keep='first')
drop_list = drop_list['uniquecode1'].to_list()

#剔除列表中重复披露的行
fund_list_snapshot_prior = fund_list_snapshot_prior[~fund_list_snapshot_prior['uniquecode1'].isin(drop_list)]

#最终列表整理
fund_list_snapshot_prior2 = pd.pivot_table(fund_list_snapshot_prior,index=["symbol"],aggfunc={'stk_mkv_ratio':np.sum,'ts_code':np.count_nonzero,'mkv':np.sum,'amount':np.sum})
fund_list_snapshot_prior2 = fund_list_snapshot_prior2.sort_values(by='stk_mkv_ratio', ascending=False)

#Export the df to excel
fund_list_snapshot2.to_excel(r'C:\Users\Austin\Desktop\Tushare\list3.xlsx', index = True)
fund_list_snapshot_prior2.to_excel(r'C:\Users\Austin\Desktop\Tushare\list2.xlsx', index = True)


