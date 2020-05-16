# -*- coding: utf-8 -*-

import Utils.Technical_indicator as Ti

#Load Tushare

import Utils.configuration_file_service as config_service
import tushare as ts

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)


df = pro.daily(ts_code='000001.SZ,600000.SH', start_date='20180701', end_date='20180718')

df2 = Ti.macd(df, n=12, m=26, k=9)

print(df2)