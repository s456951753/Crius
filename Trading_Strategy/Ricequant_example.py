# -*- coding: utf-8 -*-

from rqalpha import run_code

code = """
from rqalpha.api import *


import numpy as np
import math
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

list = ['000685.SZ', '000690.SZ', '000935.SZ', '000937.SZ', '002004.SZ', '002048.SZ',
        '002419.SZ', '002430.SZ', '002440.SZ', '002444.SZ', '002531.SZ', '002597.SZ',
        '002605.SZ', '002798.SZ', '300080.SZ', '300118.SZ', '600064.SH', '600295.SH', '600329.SH',
        '600348.SH', '600507.SH', '600682.SH', '600717.SH', '600729.SH', '600803.SH', '601107.SH',
        '601163.SH', '601330.SH', '601567.SH', '603328.SH']

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):   
#选取板块
    context.stks= TuRq.get_list_of_converted_stock_code(list)

    context.flag=True
    # 确定运行频率    
    scheduler.run_daily(rebalance)

    # 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def get_stocks(context, bar_dict):
    stocks=set([])

    for i in range(0,6): 

        # 在这个循环里，首先获取每个板块的财务数据
        fundamental_df = get_fundamentals(

            query(fundamentals.financial_indicator.adjusted_return_on_equity_weighted_average, fundamentals.eod_derivative_indicator.pb_ratio,fundamentals.eod_derivative_indicator.pe_ratio
            ).filter(
              fundamentals.income_statement.stockcode.in_(context.stks[i])
            ).filter(
              fundamentals.eod_derivative_indicator.pe_ratio<999
            ).order_by(
             fundamentals.eod_derivative_indicator.pb_ratio
            )
        )

        # 使用pandas对财务数据进行排名并打分
        df=fundamental_df.T
        df=df.sort_values('pb_ratio')
        df['pb_score']=list(range(1,len(df)+1))
        df=df.sort_values('pe_ratio')
        df['pe_score']=list(range(1,len(df)+1))
        scores=[]
        for stock in df.T.columns.values:

            scores.append(df.loc[stock,'pe_score']+df.loc[stock,'pb_score'])
        df['scores']=list(scores)
        df=df.sort_values('scores')

        #取得分最低的三个股票
        df=df.head(3)
        #logger.info(df)

        stocks = stocks | set(df.T.columns.values)
        #logger.info(i) 


    # 买入的股票，进行调仓操作
    stocks =stocks | set(fundamental_df.columns.values)
    return stocks
def rebalance(context, bar_dict):
    stocks =  get_stocks(context, bar_dict) 
    holdings = set(get_holdings(context))

    to_buy = stocks - holdings
    to_sell = holdings - stocks
    to_buy2= stocks - holdings

    for stock in to_sell:
        if bar_dict[stock].suspended == False:
            order_target_percent(stock , 0)

    if len(to_buy) == 0:
        return

    to_buy = get_trading_stocks(to_buy, context, bar_dict)
    cash = context.portfolio.cash
    total_value=context.portfolio.total_value
    if len(to_buy) >0:
        average_value = total_value *0.025
        if average_value > total_value/len(to_buy):
            average_value = total_value/len(to_buy)

    for stock in to_buy:
        if (bar_dict[stock].suspended == False)and(context.portfolio.cash>average_value):
            order_target_value(stock, average_value)
    if context.flag==True :
        sell_open('IF88', 1)
        context.flag=False

# 得到交易的股票
def get_trading_stocks(to_buy, context, bar_dict):
    trading_stocks = []
    for stock in to_buy:
        if bar_dict[stock].suspended == False:
            trading_stocks.append(stock)

    return trading_stocks

# 持仓的股票
def get_holdings(context):
    positions = context.portfolio.stock_account.positions

    holdings = []
    for position in positions:
        if positions[position].quantity > 0:
            holdings.append(position)

    return holdings
def handle_bar(context, bar_dict):
    # TODO: 开始编写你的算法吧！
    pass   
"""


config = {
  'base': {
    'start_date': '2016-06-01',
    'end_date': '2019-12-01',
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
      'stock': 1000
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
