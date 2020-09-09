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
        dbUtil.getTableName(year, "cashflow"), metadata,
        Column("id", INT, primary_key=True),
        Column("ts_code", String(10)),  # 股票代码
        Column("ann_date", String(8)),
        Column("f_ann_date", String(8)),
        Column("end_date", String(8)),
        Column("comp_type", String(3)),
        Column("report_type", String(3)),
        Column("net_profit", Float),
        Column("finan_exp", Float),
        Column("c_fr_sale_sg", Float),
        Column("recp_tax_rends", Float),
        Column("n_depos_incr_fi", Float),
        Column("n_incr_loans_cb", Float),
        Column("n_inc_borr_oth_fi", Float),
        Column("prem_fr_orig_contr", Float),
        Column("n_incr_insured_dep", Float),
        Column("n_reinsur_prem", Float),
        Column("n_incr_disp_tfa", Float),
        Column("ifc_cash_incr", Float),
        Column("n_incr_disp_faas", Float),
        Column("n_incr_loans_oth_bank", Float),
        Column("n_cap_incr_repur", Float),
        Column("c_fr_oth_operate_a", Float),
        Column("c_inf_fr_operate_a", Float),
        Column("c_paid_goods_s", Float),
        Column("c_paid_to_for_empl", Float),
        Column("c_paid_for_taxes", Float),
        Column("n_incr_clt_loan_adv", Float),
        Column("n_incr_dep_cbob", Float),
        Column("c_pay_claims_orig_inco", Float),
        Column("pay_handling_chrg", Float),
        Column("pay_comm_insur_plcy", Float),
        Column("oth_cash_pay_oper_act", Float),
        Column("st_cash_out_act", Float),
        Column("n_cashflow_act", Float),
        Column("oth_recp_ral_inv_act", Float),
        Column("c_disp_withdrwl_invest", Float),
        Column("c_recp_return_invest", Float),
        Column("n_recp_disp_fiolta", Float),
        Column("n_recp_disp_sobu", Float),
        Column("stot_inflows_inv_act", Float),
        Column("c_pay_acq_const_fiolta", Float),
        Column("c_paid_invest", Float),
        Column("n_disp_subs_oth_biz", Float),
        Column("oth_pay_ral_inv_act", Float),
        Column("n_incr_pledge_loan", Float),
        Column("stot_out_inv_act", Float),
        Column("n_cashflow_inv_act", Float),
        Column("c_recp_borrow", Float),
        Column("proc_issue_bonds", Float),
        Column("oth_cash_recp_ral_fnc_act", Float),
        Column("stot_cash_in_fnc_act", Float),
        Column("free_cashflow", Float),
        Column("c_prepay_amt_borr", Float),
        Column("c_pay_dist_dpcp_int_exp", Float),
        Column("incl_dvd_profit_paid_sc_ms", Float),
        Column("oth_cashpay_ral_fnc_act", Float),
        Column("stot_cashout_fnc_act", Float),
        Column("n_cash_flows_fnc_act", Float),
        Column("eff_fx_flu_cash", Float),
        Column("n_incr_cash_cash_equ", Float),
        Column("c_cash_equ_beg_period", Float),
        Column("c_cash_equ_end_period", Float),
        Column("c_recp_cap_contrib", Float),
        Column("incl_cash_rec_saims", Float),
        Column("uncon_invest_loss", Float),
        Column("prov_depr_assets", Float),
        Column("depr_fa_coga_dpba", Float),
        Column("amort_intang_assets", Float),
        Column("lt_amort_deferred_exp", Float),
        Column("decr_deferred_exp", Float),
        Column("incr_acc_exp", Float),
        Column("loss_disp_fiolta", Float),
        Column("loss_scr_fa", Float),
        Column("loss_fv_chg", Float),
        Column("invest_loss", Float),
        Column("decr_def_inc_tax_assets", Float),
        Column("incr_def_inc_tax_liab", Float),
        Column("decr_inventories", Float),
        Column("decr_oper_payable", Float),
        Column("incr_oper_payable", Float),
        Column("others", Float),
        Column("im_net_cashflow_oper_act", Float),
        Column("conv_debt_into_cap", Float),
        Column("conv_copbonds_due_within_1y", Float),
        Column("fa_fnc_leases", Float),
        Column("end_bal_cash", Float),
        Column("beg_bal_cash", Float),
        Column("beg_bal_cash_equ", Float),
        Column("im_n_incr_cash_equ", Float),
        Column("update_flag", String(3))
    )

def get_ts_code(engine):
    """查询ts_code"""
    return pd.read_sql('select ts_code from stock_basic', engine)

def get_ts_code_and_list_date(engine):
    """查询ts_code"""
    return pd.read_sql('select ts_code,list_date from stock_basic', engine)


def update_bulk_cashflow_by_period_and_ts_code(base_name, engine, pro, codes, start_date, end_date, retry_count=3,
                                             pause=2):
    coverage = dbUtil.getTableRange(base_name="", start_date=start_date, end_date=end_date)
    for i in coverage:
        for rownum in range(0, len(codes)):
            logger.debug("started processing data for " + codes.iloc[rownum]['ts_code'] + " for period " + i)
            if (int(codes.iloc[rownum]['list_date'][0:4]) <= int(i[1:5]) or int(
                    codes.iloc[rownum]['list_date'][0:4]) <= int(i[6:10])):
                try:
                    to_insert = pro.cashflow_vip(ts_code=codes.iloc[rownum]['ts_code'], start_date=i[1:5] + '0101',
                                               end_date=i[6:10] + '1231')
                    logger.debug("start inserting data into DB")
                    to_insert.to_sql(base_name + i, engine, if_exists='append', index=False)
                    logger.debug("end inserting data into DB")
                except Exception as e:
                    logger.error(e)
                    logger.error(
                        "error processing data for range " + str(i) + " for code " + codes.iloc[rownum]['ts_code'])


def update_bulk_cashflow_by_ts_code_and_insert_by_year(base_name, engine, pro, codes, sharding_column, failed_count=0,
                                                     failed_tolerent=3):
    failed = []
    for code in codes['ts_code']:
        logger.debug("started processing data for " + code)
        try:
            to_insert = pro.cashflow_vip(ts_code=code)
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
            failed.append(code)
            logger.error(e)
            logger.error("error processing data for code " + code)
    if (failed_count < failed_tolerent):
        logger.warning("retrying now.")
        failed_count = failed_count + 1
        update_bulk_cashflow_by_ts_code_and_insert_by_year(base_name=base_name, engine=engine, pro=pro,
                                                         codes=pd.DataFrame(failed, columns=['ts_code']),
                                                         sharding_column=sharding_column,
                                                         failed_count=failed_count)
    else:
        logger.error("the below code has failed after maximum attempts. " + ','.join(failed))

logger = logging.getLogger('cashflow_sharded')
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
# update_bulk_cashflow_by_period_and_ts_code(base_name='cashflow', engine=engine, pro=pro, codes=df, start_date='19950101',
# end_date=datetime.date.today().strftime("%Y%m%d"))
update_bulk_cashflow_by_ts_code_and_insert_by_year(base_name='cashflow', engine=engine, pro=pro, codes=df,
                                                 sharding_column='f_ann_date')
