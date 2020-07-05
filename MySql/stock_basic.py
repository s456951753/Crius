# -*- coding: utf-8 -*-

from rqalpha.api import *

import Utils.numeric_utils as TuRq
from datetime import datetime, timedelta
from datetime import date
import time as t
import pandas as pd

#Load Tushare
from rqalpha.apis.api_base import history_bars, get_position
from rqalpha.mod.rqalpha_mod_sys_accounts.api.api_stock import order_target_value, order_value

import Utils.configuration_file_service as config_service
import tushare as ts

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)


# coding=utf-8

import pandas as pd
import tushare as ts
from sqlalchemy import create_engine

from MySql.mysql_tables_structure import Base
import Utils.mysql_functions as mf

# 创建数据库引擎
engine = create_engine(config_service.getDefaultDB())
conn = engine.connect()

# 创建mysql所有表结构
Base.metadata.create_all(engine)

# 股票列表
mf.update_stock_basic(engine, pro, 3, 2)

# df = pro.stock_basic(exchange='', list_status='L',
# fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')

# print(df)
