#找出列表中重复披露的行,取最近的日期
# -*- coding: utf-8 -*-

import numpy as np
import math
import Utils.numeric_utils as TuRq
from datetime import date, datetime, timedelta
import datetime as dt
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

import logging

logger =logging.getLogger('Trading_small_quality_cap')
token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)

# 选择我们感兴趣的股票
small_cap_cutoff_up = 1150000  # defind the cutoff for small caps upper end （unit=万元）Note the cutoff is consistent with MSCI small cap definition
small_cap_cutoff_low = 50000  # defind the cutoff for small caps lower end （unit=万元）
pe_cutoff_up = 30  # defind the cutoff for stock PE ratio

# 剔除过去x天内有涨停的的股票
daysx = 5

TIME_PERIOD = 14
HIGH_RSI = 80
LOW_RSI = 25
ORDER_PERCENT = 0.1

# 对我们选中的股票集合进行loop，运算每一只股票的RSI数值
d0 = dt.datetime.today()
snapshot_date = d0.strftime("%Y%m%d")

sector_full_list_snapshot = pro.query('daily_basic', ts_code='', trade_date=snapshot_date,
                                      fields='ts_code,turnover_rate_f,volume_ratio,pe_ttm,dv_ratio,free_share,total_mv')

# 以股票的 市值(mv) 和 市盈率(PE) 进行筛选
list1 = sector_full_list_snapshot[
    sector_full_list_snapshot['total_mv'].between(small_cap_cutoff_low, small_cap_cutoff_up) &
    sector_full_list_snapshot['pe_ttm'].between(0.01, pe_cutoff_up)]

list1.to_excel(r'C:\Users\Austin\Desktop\Tushare\list1.xlsx', index = True)

# 剔除过去x天内有涨停的的股票 (x 在init 定义）

up_start_date = d0 - timedelta(days = daysx)
up_start_date = up_start_date.strftime("%Y%m%d")

up_end_date = d0 - timedelta(days=1)
up_end_date = up_end_date.strftime("%Y%m%d")

up_list = pro.limit_list(start_date=up_start_date, end_date=up_end_date)
up_list = up_list['ts_code'].to_list()

list2 = list1[~list1.ts_code.isin(up_list)]

list2.to_excel(r'C:\Users\Austin\Desktop\Tushare\list2.xlsx', index = True)

# filter on stocks with at least three years trading history #TODO: the three year variable should be an input field 730 改为人工输入变量，以年为单位
list_days_filter = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,list_date')
list_days_filter['list_date'] = pd.to_datetime(list_days_filter['list_date'], format='%Y%m%d')
list_days_filter['snapshot_date'] = snapshot_date
list_days_filter['snapshot_date'] = pd.to_datetime(list_days_filter['snapshot_date'], format='%Y%m%d')
list_days_filter['list_days'] = (list_days_filter['snapshot_date'] - list_days_filter['list_date']).dt.days
list_days_filter2 = list_days_filter[list_days_filter['list_days'] > 730]
list_days_filter2 = list_days_filter2['ts_code'].to_list()

list3 = list2[~list2.ts_code.isin(list_days_filter2)]

list3.to_excel(r'C:\Users\Austin\Desktop\Tushare\list3.xlsx', index = True)

list3 = list3['ts_code'].to_list()


stocks = TuRq.get_list_of_converted_stock_code(list3)

#print(stocks)