# -*- coding: utf-8 -*-

from rqalpha import run_code

code = """
from rqalpha.api import *


import numpy as np
import math
import Utils.numeric_utils as TuRq
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

import logging

import builtins
logger =logging.getLogger('Trading_small_quality_cap')
token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):

    # 选择我们感兴趣的股票
    context.small_cap_cutoff_up = 1150000 #defind the cutoff for small caps upper end （unit=万元）Note the cutoff is consistent with MSCI small cap definition
    context.small_cap_cutoff_low = 50000 #defind the cutoff for small caps lower end （unit=万元）
    context.pe_cutoff_up = 30 #defind the cutoff for stock PE ratio
    
    #剔除过去x天内有涨停的的股票
    context.daysx = 5
    
    context.TIME_PERIOD = 14
    context.HIGH_RSI = 80
    context.LOW_RSI = 30
    context.ORDER_PERCENT = 0.1


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):

    # 对我们选中的股票集合进行loop，运算每一只股票的RSI数值
    d0 = context.now.date()
    snapshot_date = d0.strftime("%Y%m%d")
    
    sector_full_list_snapshot = pro.query('daily_basic', ts_code='', trade_date=snapshot_date,fields='ts_code,turnover_rate_f,volume_ratio,pe_ttm,dv_ratio,free_share,total_mv')
    
    #以股票的 市值(mv) 和 市盈率(PE) 进行筛选
    list1 = sector_full_list_snapshot[sector_full_list_snapshot['total_mv'].between(context.small_cap_cutoff_low, context.small_cap_cutoff_up) & sector_full_list_snapshot['pe_ttm'].between(0.01, context.pe_cutoff_up)]
    
    #剔除过去x天内有涨停的的股票 (x 在init 定义）
    
    up_start_date = d0 - timedelta(days=context.daysx)
    up_start_date = up_start_date.strftime("%Y%m%d")
    
    up_end_date = d0 - timedelta(days=1)
    up_end_date = up_end_date.strftime("%Y%m%d") 

    up_list = pro.limit_list(start_date=up_start_date, end_date=up_end_date)
    up_list = up_list['ts_code'].to_list()

    list2 = list1[~list1.ts_code.isin(up_list)]

    #filter on stocks with at least three years trading history #TODO: the three year variable should be an input field 730 改为人工输入变量，以年为单位
    list_days_filter = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,list_date')
    list_days_filter['list_date'] = pd.to_datetime(list_days_filter['list_date'],format='%Y%m%d')
    list_days_filter['snapshot_date'] = snapshot_date
    list_days_filter['snapshot_date'] = pd.to_datetime(list_days_filter['snapshot_date'],format='%Y%m%d')
    list_days_filter['list_days'] = (list_days_filter['snapshot_date'] - list_days_filter['list_date']).dt.days
    list_days_filter2 = list_days_filter[list_days_filter['list_days'] > 730]
    list_days_filter2 = list_days_filter2['ts_code'].to_list()

    list3 = list2[~list2.ts_code.isin(list_days_filter2)]
    
    list3 = list3['ts_code'].to_list()
    
    context.stocks = TuRq.get_list_of_converted_stock_code(list3)
    print("begin filtering")
    
    for stock in context.stocks:
        print('processing stock:'+stock)
        # The start date of tushare data retrieving
        start_date=(context.now-timedelta(days=30)).strftime('%Y%m%d')    

        # 读取历史数据
        # prices = history_bars(stock, context.TIME_PERIOD+1, '1d', 'close')
        # replace rqalpha data with tushare data
        tusharestock = TuRq.get_converted_stock_code(stock)
        prices = pro.daily(ts_code=tusharestock,start_date=start_date,end_date=snapshot_date)
        
        # 用Talib计算RSI值
        if prices.empty:
            continue    
        print(prices['close'])
        rsi_data = talib.RSI(prices['close'], timeperiod=context.TIME_PERIOD).tolist()[-1]
        print(rsi_data)
        cur_position = get_position(stock).quantity
        print("用剩余现金的x%来购买新的股票")
        target_available_cash = context.portfolio.cash * context.ORDER_PERCENT

        print("当RSI大于设置的上限阀值，清仓该股票")
        if rsi_data > context.HIGH_RSI and cur_position > 0:
            order_target_value(stock, 0)

        print("当RSI小于设置的下限阀值，用剩余cash的一定比例补仓该股")
        if rsi_data < context.LOW_RSI:
            logger.info("target available cash caled: " + str(target_available_cash))
            print("如果剩余的现金不够一手 - 100shares，那么会被ricequant 的order management system reject掉")
            order_value(stock, target_available_cash)

"""

config = {
    'base': {
        'start_date': '2016-06-01',
        'end_date': '2016-08-11',
        # 回测频率，1d, 1m, tick
        'frequency': '1d',
        # 回测所需 bundle 数据地址，可设置为 RQPro 终端【个人设置】的【数据下载路径】
        #    'data_bundle_path': './bundle',
        # 策略文件地址
        #    'strategy_file': './strategy.py',
        # 保证金倍率。基于基础保证金水平进行调整
        'margin_multiplier': 1,
        # 运行类型。b 为回测，p 为模拟交易，r 为实盘交易
        'run_type': 'b',
        # 基准合约
        'benchmark': '000300.XSHG',

        # 账户类别及初始资金
        'accounts': {
            'stock': 1000000
        },
    },
    'extra': {
        # 是否开启性能分析
        'enable_profiler': False,
        # 输出日志等级，有 verbose, info, warning, error 等选项，可以通过设置为 verbose 来查看最详细日志
        'log_level': 'verbose',
    },
    'mod': {
        # 模拟撮合模块
        'sys_simulation': {
            'enabled': True,
            # 是否开启信号模式。如果开启，限价单将按照指定价格成交，并且不受撮合成交量限制
            'signal': False,
            # 撮合方式。current_bar 当前 bar 收盘价成交，next_bar 下一 bar 开盘价成交，best_own 己方最优价格成交（tick 回测使用）
            # best_counterparty 对手方最优价格成交（tick 回测使用），last 最新价成交（tick 回测使用）
            'matching_type': 'current_bar',
            # 是否允许涨跌停状态下买入、卖出
            'price_limit': False,
            # 是否开启成交量限制
            'volume_limit': True,
            # 按照 bar 数据成交量的一定比例进行限制，超限部分无法在当前 bar 一次性撮合成交
            'volume_percent': 0.25,
            # 滑点模型。PriceRatioSlippage 为基于价格比例的滑点模型，TickSizeSlippage 为基于最小价格变动单位的滑点模型
            'slippage_model': 'PriceRatioSlippage',
            # 滑点值
            'slippage': 0,
        },
        # 风控模块
        'sys_risk': {
            'enabled': True,
            # 检查可用资金是否足够
            'validate_cash': True,
            # 检查可平仓位是否足够
            'validate_position': True,
        },
        # 分析模块
        'sys_analyser': {
            'enabled': True,
            # 是否画图
            'plot': True,
            # 指定输出回测报告 csv 路径
            'report_save_path': None,
        },
        'sys_transaction_cost': {
            'enabled': True,
            # 设置最小佣金费用
            'cn_stock_min_commission': 5,
            # 佣金倍率
            'commission_multiplier': 1,
        }
    }
}

run_code(code, config)
