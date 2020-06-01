#找出列表中重复披露的行,取最近的日期
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

#本季度和上一季度基金公司持股文件读取
fund_list = pd.read_excel (r'C:\Users\Austin\Desktop\Tushare\fund_list_snapshot.xlsx', index = False)
fund_list_prior = pd.read_excel (r'C:\Users\Austin\Desktop\Tushare\fund_list_snapshot_prior.xlsx', index = False)

#上季度列名称改名，防止重复
fund_list_prior = fund_list_prior.rename(columns={'amount': 'amount_p', 'mkv': 'mkv_p', 'stk_float_ratio': 'stk_float_ratio_p', 'ts_code': 'ts_code_p'})

#合并两个基金表格
#summary_fund_list = pd.concat([fund_list, fund_list_prior], axis=1, join='outer', sort=False)

summary_fund_list = pd.merge(fund_list, fund_list_prior, on='symbol', how='outer')
summary_fund_list = summary_fund_list.fillna(0)

#计算两个基金表格，寻找差值
summary_fund_list['stk_float_ratio_diff'] = summary_fund_list['stk_float_ratio'] - summary_fund_list['stk_float_ratio_p']
summary_fund_list = summary_fund_list.sort_values(by='stk_float_ratio_diff', ascending=False)

#剔除港股，增加申万分类
summary_fund_list['exchange'] = summary_fund_list['symbol'].str[-2:]
summary_fund_list = summary_fund_list[~summary_fund_list.symbol.str.contains('HK')]

SW_index_list = fund_list = pd.read_excel (r'C:\Users\Austin\Desktop\Tushare\SW_index_list.xlsx', sheet_name='Constituent', index = False)
SW_index_list = SW_index_list.loc[:, ['symbol','industry_name_lv1']]

summary_fund_list2 = pd.merge(summary_fund_list, SW_index_list, on = 'symbol', how = 'left')

#Export the df to excel
summary_fund_list2.to_excel(r'C:\Users\Austin\Desktop\Tushare\summary_fund_list2.xlsx', index = True)


