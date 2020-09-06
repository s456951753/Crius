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


def getTableMeta(year: int, metadata: MetaData) -> Table:
    """
    get corresponding table meta data.
    :param year: year of the data
    :return: a Table object representing the table structure
    """
    return Table(
        dbUtil.getTableName(year, "income"), metadata,
        Column("id", INT, primary_key=True),
        Column("ts_code", String(10)),  # 股票代码
        Column("ann_date", String(8)),
        Column("f_ann_date", String(8)),
        Column("end_date", String(8)),
        Column("report_type", String(3)),
        Column("comp_type", String(3)),
        Column("basic_eps", Float),
        Column("diluted_eps", Float),
        Column("total_revenue", Float),
        Column("revenue", Float),
        Column("int_income", Float),
        Column("prem_earned", Float),
        Column("comm_income", Float),
        Column("n_commis_income", Float),
        Column("n_oth_income", Float),
        Column("n_oth_b_income", Float),
        Column("prem_income", Float),
        Column("out_prem", Float),
        Column("une_prem_reser", Float),
        Column("reins_income", Float),
        Column("n_sec_tb_income", Float),
        Column("n_sec_uw_income", Float),
        Column("n_asset_mg_income", Float),
        Column("oth_b_income", Float),
        Column("fv_value_chg_gain", Float),
        Column("invest_income", Float),
        Column("ass_invest_income", Float),
        Column("forex_gain", Float),
        Column("total_cogs", Float),
        Column("oper_cost", Float),
        Column("int_exp", Float),
        Column("comm_exp", Float),
        Column("biz_tax_surchg", Float),
        Column("sell_exp", Float),
        Column("admin_exp", Float),
        Column("fin_exp", Float),
        Column("assets_impair_loss", Float),
        Column("prem_refund", Float),
        Column("compens_payout", Float),
        Column("reser_insur_liab", Float),
        Column("div_payt", Float),
        Column("reins_exp", Float),
        Column("oper_exp", Float),
        Column("compens_payout_refu", Float),
        Column("insur_reser_refu", Float),
        Column("reins_cost_refund", Float),
        Column("other_bus_cost", Float),
        Column("operate_profit", Float),
        Column("non_oper_income", Float),
        Column("non_oper_exp", Float),
        Column("nca_disploss", Float),
        Column("total_profit", Float),
        Column("income_tax", Float),
        Column("n_income", Float),
        Column("n_income_attr_p", Float),
        Column("minority_gain", Float),
        Column("oth_compr_income", Float),
        Column("t_compr_income", Float),
        Column("compr_inc_attr_p", Float),
        Column("compr_inc_attr_m_s", Float),
        Column("ebit", Float),
        Column("ebitda", Float),
        Column("insurance_exp", Float),
        Column("undist_profit", Float),
        Column("distable_profit", Float),
        Column("update_flag", String(3))
    )

def get_ts_code(engine):
    """查询ts_code"""
    return pd.read_sql('select ts_code from stock_basic', engine)

def get_ts_code_and_list_date(engine):
    """查询ts_code"""
    return pd.read_sql('select ts_code,list_date from stock_basic', engine)


def update_bulk_income_by_period_and_ts_code(base_name, engine, pro, codes, start_date, end_date, retry_count=3,
                                             pause=2):
    coverage = dbUtil.getTableRange(base_name="", start_date=start_date, end_date=end_date)
    for i in coverage:
        for rownum in range(0, len(codes)):
            logger.debug("started processing data for " + codes.iloc[rownum]['ts_code'] + " for period " + i)
            if (int(codes.iloc[rownum]['list_date'][0:4]) <= int(i[1:5]) or int(
                    codes.iloc[rownum]['list_date'][0:4]) <= int(i[6:10])):
                try:
                    to_insert = pro.income_vip(ts_code=codes.iloc[rownum]['ts_code'], start_date=i[1:5] + '0101',
                                               end_date=i[6:10] + '1231')
                    logger.debug("start inserting data into DB")
                    to_insert.to_sql(base_name + i, engine, if_exists='append', index=False)
                    logger.debug("end inserting data into DB")
                except Exception as e:
                    logger.error(e)
                    logger.error(
                        "error processing data for range " + str(i) + " for code " + codes.iloc[rownum]['ts_code'])


def update_bulk_income_by_ts_code_and_insert_by_year(base_name, engine, pro, codes, sharding_column, failed_count=0,
                                                     failed_tolerent=3):
    failed = []
    for code in codes['ts_code']:
        logger.debug("started processing data for " + code)
        try:
            to_insert = pro.income_vip(ts_code=code)
            logger.debug("start inserting data into DB")
            distinct_years = set(to_insert[sharding_column].str[0:4])
            for year in distinct_years:
                year_section = to_insert[to_insert[sharding_column].str[0:4] == year]
                if (year == None):
                    year = 9999
                    year_section = to_insert[pd.isna(to_insert[sharding_column]) == True]
                year_section.to_sql(dbUtil.getTableName(int(year), base_name=base_name), engine, if_exists='append',
                                    index=False)
            logger.debug("end inserting data into DB")
        except Exception as e:
            failed_count = failed_count + 1
            failed.append(code)
            logger.error(e)
            logger.error("error processing data for code " + code)
    if (failed_count < failed_tolerent):
        logger.warning("retrying now.")
        update_bulk_income_by_ts_code_and_insert_by_year(base_name=base_name, engine=engine, pro=pro,
                                                         codes=pd.DataFrame(failed, columns=['ts_code']),
                                                         sharding_column=sharding_column,
                                                         failed_count=failed_count)
    else:
        logger.error("the below code has failed after maximum attempts. " + ','.join(failed))

logger = logging.getLogger('income_sharded')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setStream(sys.stdout)
fi = logging.FileHandler(filename="../engine.log")

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
fi.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(fi)

engine = create_engine(config_service.getDefaultDB())
conn = engine.connect()

metadata = MetaData()

years = dbUtil.getYears()
for i in years.keys():
    getTableMeta(i, metadata)

metadata.create_all(engine)

# df = get_ts_code_and_list_date(engine)
df = get_ts_code(engine)
# update_bulk_income_by_period_and_ts_code(base_name='income', engine=engine, pro=pro, codes=df, start_date='19950101',
# end_date=datetime.date.today().strftime("%Y%m%d"))
update_bulk_income_by_ts_code_and_insert_by_year(base_name='income', engine=engine, pro=pro, codes=df,
                                                 sharding_column='f_ann_date')
