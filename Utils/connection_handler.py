from typing import Dict, Any

import pandas
from tushare.pro.client import DataApi
import logging
import time

log = logging.getLogger("connection manager")


def call_tushare_api(data_Api: DataApi, api_name, fields, retry_Count=3, retry_mode="linear",
                     **kwargs):
    """
    a wrapper to call tushare api with retry. return none if errors out in all attempts
    :param api_name: the tushare api name you use
    :param fields: what you fill in as fields for tushare's api caller
    :param data_Api: the tushare dataapi object, normally named pro
    :param retry_Count: count of retries you want to attempt. default to 3
    :param retry_mode: how you want retry delay to be calculated. two options are available: linear or exp (exponential).
        default to linear.
    :param kwargs: other parameters for tushareApi, will be passed directly to tushare API caller
    :return: dataframe containing requested data, or empty data frame
    """
    already_retry_count = 1
    success = False
    data = pandas.DataFrame.empty
    while (already_retry_count <= retry_Count):
        try:
            data = data_Api.query(api_name, fields, kwargs)
            success = True
        except:
            already_retry_count = already_retry_count + 1
            log.warning(msg="connection to " +
                            api_name + " has failed. Attempt " + str(already_retry_count))
            if (retry_mode == "linear"):
                time.sleep(30 * str(already_retry_count))
                continue
            elif (retry_mode == "exp"):
                time.sleep(30 * 2 ^ str(already_retry_count))
                continue
            else:
                time.sleep(30)
                continue
    if (not success):
        log.warning("connection to " + api_name + " has failed.")
    return data


import Utils.configuration_file_service as config_service
import tushare as ts
import datetime

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)
call_tushare_api(api_name='daily_basic', data_Api=pro, ts_code='', trade_date=datetime.date.today().strftime("%Y%m%d"),
                 fields='ts_code,turnover_rate_f,volume_ratio,pe_ttm,dv_ratio,free_share,total_mv')
