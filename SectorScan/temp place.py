# -*- coding: utf-8 -*-

from rqalpha import run_code

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
token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)

df = ts.pro_bar(ts_code='000001.SZ', adj='hfq', start_date='20180101', end_date='20181011')

print(df)