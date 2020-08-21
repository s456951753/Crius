# -*- coding: utf-8 -*-

#Load Tushare

import Utils.configuration_file_service as config_service
import tushare as ts
import time

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)


df = pro.query('trade_cal', start_date='19000101', end_date='20011231')

print(df)