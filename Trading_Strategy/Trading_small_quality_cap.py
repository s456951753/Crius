# -*- coding: utf-8 -*-

from rqalpha import run_code

code = """
from rqalpha.api import *

import Utils.numeric_utils as TuRq
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


#Setup - fundamental section
snapshot_date = '20200515'
small_cap_cutoff_up = 1150000 #defind the cutoff for small caps upper end （unit=万元）Note the cutoff is consistent with MSCI small cap definition
small_cap_cutoff_low = 0 #defind the cutoff for small caps lower end （unit=万元）
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


#remove stocks that had up limited in the last x days 剔除过去N天内有涨停的的股票
up_start_date = 20200511 #TODO: this part to be automated later, reference snapshot_date. 改为自动化，这个日期应为 snapshot_date - N天. N 为人工输入
up_end_date = 20200515 #TODO: this part to be automated later reference snapshot_date。 改为自动化，这个日期应为 snapshot_date 前一天

up_list = pro.limit_list(start_date=up_start_date, end_date=up_end_date)['ts_code']

templist2 = templist1[~templist1.ts_code.isin(up_list)]
t.sleep(1)

#filter on stocks with at least three years trading history #TODO: the three year variable should be an input field 730 改为人工输入变量，以年为单位
list_days_filter = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,list_date')
list_days_filter['list_date'] = pd.to_datetime(list_days_filter['list_date'],format='%Y%m%d')
list_days_filter['snapshot_date'] = snapshot_date
list_days_filter['snapshot_date'] = pd.to_datetime(list_days_filter['snapshot_date'],format='%Y%m%d')
list_days_filter['list_days'] = (list_days_filter['snapshot_date'] - list_days_filter['list_date']).dt.days
list_days_filter2 = list_days_filter[list_days_filter['list_days'] > 730]

templist3 = templist2[~templist2.ts_code.isin(list_days_filter2)]

templist4 =templist3['ts_code'].tolist()

templist5 = TuRq.get_list_of_converted_stock_code(templist4)

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    context.s1 = templist5

    # 设置这个策略当中会用到的参数，在策略中可以随时调用，这个策略使用长短均线，我们在这里设定长线和短线的区间，在调试寻找最佳区间的时候只需要在这里进行数值改动
    context.SHORTPERIOD = 14
    context.LONGPERIOD = 60


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑
    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # 因为策略需要用到均线，所以需要读取历史数据
    prices = history_bars(context.s1, context.LONGPERIOD+1, '1d', 'close')

    # 使用talib计算长短两根均线，均线以array的格式表达
    short_avg = talib.SMA(prices, context.SHORTPERIOD)
    long_avg = talib.SMA(prices, context.LONGPERIOD)

    plot("short avg", short_avg[-1])
    plot("long avg", long_avg[-1])

    # 计算现在portfolio中股票的仓位
    cur_position = get_position(context.s1).quantity
    # 计算现在portfolio中的现金可以购买多少股票
    shares = context.portfolio.cash / bar_dict[context.s1].close

    # 如果短均线从上往下跌破长均线，也就是在目前的bar短线平均值低于长线平均值，而上一个bar的短线平均值高于长线平均值
    if short_avg[-1] - long_avg[-1] < 0 and short_avg[-2] - long_avg[-2] > 0 and cur_position > 0:
        # 进行清仓
        order_target_value(context.s1, 0)

    # 如果短均线从下往上突破长均线，为入场信号
    if short_avg[-1] - long_avg[-1] > 0 and short_avg[-2] - long_avg[-2] < 0:
        # 满仓入股
        order_shares(context.s1, shares)


"""

config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2019-12-01",
    "benchmark": "000300.XSHG",
    "accounts": {
      "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}

run_code(code, config)

#TODO:　动态复权　就是以策略回测当前日期为基准进行前复权。目的是为了更贴近真实的交易环境。 　