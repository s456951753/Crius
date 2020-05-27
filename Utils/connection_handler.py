import pandas
from tushare.pro.client import DataApi
import logging
import time

log = logging.getLogger("connection manager")


def call_tushare_api(self, data_Api: DataApi, query_parameters: dict, retry_Count=3, retry_mode="linear", **kwargs):
    """
    a wrapper to call tushare api with retry. return none if errors out in all attempts
    :param data_Api: the tushare dataapi object, normally named pro
    :param query_parameters: a dictionary containing compulsary query parameters of tushare api, including api_name
        and fields
    :param retry_Count: count of retries you want to attempt. default to 3
    :param retry_mode: how you want retry delay to be calculated. two options are available: linear or exp (exponential).
        default to linear.
    :param kwargs: other parameters for tushareApi, will be passed directly to tushare API caller
    :return: dataframe containing requested data, or none
    """
    already_retry_count = 0
    success = False
    data = pandas.DataFrame.empty
    while (already_retry_count < retry_Count):
        try:
            data = data_Api.query(query_parameters.get("api_name"), query_parameters.get("fields"), kwargs)
            success = True
        except:
            already_retry_count = already_retry_count + 1
            log.warning(msg="connection to " + query_parameters.get(
                "api_name") + " has failed. Attempt " + already_retry_count - 1)
            if (retry_mode == "linear"):
                time.sleep(30 * already_retry_count)
            elif (retry_mode == "exp"):
                time.sleep(30 * 2 ^ already_retry_count)
            else:
                time.sleep(30)
    if (not success):
        log.warning("connection to " + query_parameters.get("api_name") + " has failed.")
    return data
