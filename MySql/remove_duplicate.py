"""
Refactored so more suitable for sharded daily qfq data table
"""
import sys
import time
import datetime
import logging

from sqlalchemy.exc import IntegrityError

import Utils.configuration_file_service as config_service
import Utils.DB_utils as dbUtil

import pandas as pd
import tushare as ts
from sqlalchemy import Column, String, Float, MetaData, Table, create_engine, INT

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)

engine = create_engine(config_service.getDefaultDB())
conn = engine.connect()

start_date = 20150101
end_date = 20191231

ts_code_list = pd.read_sql('select ts_code from stock_basic',engine)["ts_code"]

cal_date_list = pro.trade_cal(start_date=start_date, end_date=end_date, is_open='1')["cal_date"]

table_name = "new_daily_2015_2019"

#for ts_code in ts_code_list:
#    for date in cal_date_list:
#        df=pd.read_sql("select ts_code, trade_date from "+ table_name + " where " + "ts_code=\"" + ts_code+ "\" and trade_date between "
#                       + str(start_date) + " and " + str(end_date),engine)
#        print(df)


df=pd.read_sql("select ts_code, trade_date, count(*) from new_daily_2015_2019 group by ts_code, trade_date having count(*) > 1",engine)
print(df)

df2=pd.read_sql("select id from new_daily_2015_2019",engine)
print(df2)


#cursor = engine.cursor()