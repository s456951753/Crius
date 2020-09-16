import sys

import pandas as pd
import logging

from sqlalchemy import create_engine

import Utils.configuration_file_service as config_service
import Utils.DB_utils as dbUtil
import tushare as ts


def get_ts_code_and_list_date(engine):
    return pd.read_sql('select ts_code,list_date from stock_basic', engine)


def get_trade_cal(pro, start_date, end_date):
    return pro.trade_cal(start_date=start_date, end_date=end_date, is_open='1')["cal_date"]


def get_suspended_day_count(pro, ts_code, start_date, end_date):
    df = pro.query('suspend', ts_code=ts_code, suspend_date=start_date, resume_date=end_date,
                   fields='ts_code,suspend_date')
    return df.size


def check_integrity_daily_data_table(base_name: str, engine, pro):
    """

    :param base_name:
    :param engine:
    :return:
    """
    missing = {}
    codes = get_ts_code_and_list_date(engine)
    years = dbUtil.getYears()
    table_range = {}
    for start_year in years.keys():
        table_range[int(str(start_year) + "0101")] = int(str(years.get(start_year)) + "1231")
    for table_start in table_range.keys():
        table_end = table_range.get(table_start)
        for code in codes['ts_code']:
            list_date = int(codes[codes['ts_code'] == code]['list_date'])
            if list_date > table_end:
                # if list date after end of table, there should be no lines here
                pass
            elif table_start <= list_date <= table_end:
                df = get_from_table_by_tscode_and_tradedateint(
                    table_name=base_name + "_" + str(table_start)[0:4] + "_" + str(table_end)[0:4],
                    ts_code=code, start_date=list_date, end_date=table_end, engine=engine)
                # trade_cal = list(map(int,get_trade_cal(pro,str(list_date),str(table_end))))
                # standard_size=len(list(filter(lambda x:list_date<=x<=int(table_end),trade_cal)))
                standard_date = list(map(int, get_trade_cal(pro, str(list_date), str(table_end))))
                standard_size = len(standard_date)
                suspend_day_count = get_suspended_day_count(pro=pro, ts_code=code, start_date=str(list_date),
                                                            end_date=str(table_end))
                db_data_size = df['trade_date_int'].size
                if db_data_size + suspend_day_count < standard_size:
                    # dates in database
                    existing_dates = df['trade_date_int']
                    # existing dates that doesn't exist in dates as standard calendar
                    missing_dates = [i for i in standard_date if i not in list(existing_dates)]
                    re_capture_result = get_missing_dates(pro=pro, engine=engine, ts_code=code, dates=missing_dates,
                                                          interface_type=base_name)
                    if (re_capture_result.get('missing_from_tushare') > 0):
                        logger.debug(
                            str(re_capture_result.get('missing_from_tushare')) + " lines of data missing for " +
                            code + " between date " + str(list_date) +
                            " and " + str(table_end) + " are also missing from tushare")
                    if (re_capture_result.get('number_of_inserted_rows') > 0):
                        logger.debug(
                            str(re_capture_result.get(
                                'number_of_inserted_rows')) + " lines of data missing from db for " +
                            code + " between date " + str(list_date) +
                            " and " + str(table_end) + " have been inserted into db")
                elif db_data_size + suspend_day_count == standard_size:
                    logger.debug(
                        code + " for table " + base_name + " " + str(list_date) + " " + str(table_end)) + " is correct"
                elif db_data_size + suspend_day_count > standard_size:
                    logger.error(
                        "Data duplicate for " + code + " between date " + str(list_date) + " and " + str(table_end))


def get_from_table_by_tscode_and_tradedateint(table_name, ts_code: str, start_date: int, end_date: int,
                                              engine) -> pd.DataFrame:
    return pd.read_sql(
        "select ts_code, trade_date_int from " + table_name + " where " + "ts_code=\"" + ts_code + "\" and trade_date between "
        + str(start_date) + " and " + str(end_date), engine)


def get_missing_dates(pro, engine, ts_code, dates, interface_type):
    missing_from_tushare = 0
    number_of_inserted_rows = 0
    for date in dates:
        if (interface_type == 'daily'):
            df = pro.daily(ts_code=ts_code, start_date=date, end_date=date)
            if df.empty:
                missing_from_tushare = missing_from_tushare + 1
            else:
                df.to_sql(dbUtil.getTableName(int(date[0:4]), "daily"), engine, if_exists='append', index=False)
                number_of_inserted_rows = number_of_inserted_rows + 1

    return {"missing_from_tushare": missing_from_tushare, "number_of_inserted_rows": number_of_inserted_rows}


logger = logging.getLogger("data_integrity_check")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setStream(sys.stdout)
fi = logging.FileHandler(filename="../data_integrity_check.log")

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
fi.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(fi)

engine = create_engine(config_service.getDefaultDB())

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)

# 956-917
# get_suspended_day_count(pro,'000001.SZ','19900101','19941231')
check_integrity_daily_data_table("daily", engine=engine, pro=pro)
# df = pro.daily(trade_date='19910411',ts_code='000001.SZ',fields='ts_code,trade_date')
# print(df)
