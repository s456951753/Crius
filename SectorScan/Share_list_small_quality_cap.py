# -*- coding: utf-8 -*-

from rqalpha.api import *
from datetime import datetime, timedelta
import time as t
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import talib

import tushare as ts
token='3c311a0c0eb056bfe6c27a161e6cab275649b74245cfd5679a75dca9'
pro=ts.pro_api(token)

#Setup - fundamental section
snapshot_date = '20200507'
small_cap_cutoff_up = 1150000 #defind the cutoff for small caps upper end （unit=万元）Note the cutoff is consistent with MSCI small cap definition
small_cap_cutoff_low = 1050000 #defind the cutoff for small caps lower end （unit=万元）
pe_cutoff_up = 30 #defind the cutoff for stock PE ratio

#Setup - technical section


#Extract basic stock information
#sector_full_list = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,is_hs')


#Extract basic stock information - company introduction
#sector_full_list_intro = pro.stock_company(exchange='SZSE', fields='ts_code,chairman,manager,secretary,website,introduction,main_business')

#get daily metrics
sector_full_list_snapshot = pro.query('daily_basic', ts_code='', trade_date=snapshot_date,
                                      fields='ts_code,turnover_rate_f,volume_ratio,pe_ttm,dv_ratio,free_share,total_mv')

#Select small cap stocks with pre-defined cutoffs and with pre-defined PE range
templist1 = sector_full_list_snapshot[sector_full_list_snapshot['total_mv'].between(small_cap_cutoff_low, small_cap_cutoff_up) & sector_full_list_snapshot['pe_ttm'].between(0.01, pe_cutoff_up)]


#remove stocks that had up limited in the last x days
up_start_date = 20200424 #TODO: this part to be automated later, reference snapshot_date
up_end_date = 20200507 #TODO: this part to be automated later reference snapshot_date

up_list = pro.limit_list(start_date=up_start_date, end_date=up_end_date)['ts_code']

templist2 = templist1[~templist1.ts_code.isin(up_list)]
t.sleep(1)

#filter on stocks with at least three years trading history #TODO: the three year variable shoudl be an input field
list_days_filter = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,list_date')
list_days_filter['list_date'] = pd.to_datetime(list_days_filter['list_date'],format='%Y%m%d')
list_days_filter['snapshot_date'] = snapshot_date
list_days_filter['snapshot_date'] = pd.to_datetime(list_days_filter['snapshot_date'],format='%Y%m%d')
list_days_filter['list_days'] = (list_days_filter['snapshot_date'] - list_days_filter['list_date']).dt.days
list_days_filter2 = list_days_filter[list_days_filter['list_days'] > 730]

templist3 = templist2[~templist2.ts_code.isin(list_days_filter2)]

templist4 =templist3['ts_code'].tolist()

print(templist4)

#get multi-year key financial info then covert to dataframe
fina_start_date = 20170930 #TODO: this part to be automated later, reference snapshot_date
fina_end_date = 20191231 #TODO: this part to be automated later reference snapshot_date

fin_data = {} #TODO: Not working yet
for ticker in templist4:
    fin_data = pro.query('fina_indicator_vip', ts_code=ticker, start_date=fina_start_date, end_date=fina_end_date,
                         fields='ts_code,end_date,debt_to_eqt,roe_avg,gross_margin,ebt_yoy')

fin_data_list = pd.DataFrame({stockitem: data['ts_code,end_date,debt_to_eqt,roe_avg,gross_margin,ebt_yoy']
                    for stockitem, data in fin_data.items()})
#TODO: the above section is not working yet

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):

    # 选择我们感兴趣的股票
    context.stocks = templist4

    context.TIME_PERIOD = 14
    context.HIGH_RSI = 85
    context.LOW_RSI = 30
    context.ORDER_PERCENT = 0.3

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！

    # 对我们选中的股票集合进行loop，运算每一只股票的RSI数值
    for stock in context.stocks:
        # 读取历史数据
        prices = history_bars(stock, context.TIME_PERIOD+1, '1d', 'close')

        # 用Talib计算RSI值
        rsi_data = talib.RSI(prices, timeperiod=context.TIME_PERIOD)[-1]

        cur_position = get_position(stock).quantity
        # 用剩余现金的30%来购买新的股票
        target_available_cash = context.portfolio.cash * context.ORDER_PERCENT

        # 当RSI大于设置的上限阀值，清仓该股票
        if rsi_data > context.HIGH_RSI and cur_position > 0:
            order_target_value(stock, 0)

        # 当RSI小于设置的下限阀值，用剩余cash的一定比例补仓该股
        if rsi_data < context.LOW_RSI:
            logger.info("target available cash caled: " + str(target_available_cash))
            # 如果剩余的现金不够一手 - 100shares，那么会被ricequant 的order management system reject掉
            order_value(stock, target_available_cash)


#Export the df to excel
#fin_data.to_excel(r'C:\Users\Austin\Desktop\Tushare\list2.xlsx', index = False)
