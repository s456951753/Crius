# -*- coding: utf-8 -*-


from datetime import date, datetime, timedelta
import time as t
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import talib

#Load Tushare
from rqalpha.apis.api_base import history_bars, get_position
from rqalpha.mod.rqalpha_mod_sys_accounts.api.api_stock import order_target_value, order_value

import Utils.configuration_file_service as config_service
import tushare as ts

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)

import Utils.numeric_utils as TuRq

#df2 = pro.index_classify(level='L2', src='SW')


#财务指标数据
list = ['20191231','20190630','20181231','20180630','20171231','20170630']

appended_data = []
for dates in list:
    all_data = pro.fina_indicator_vip(period=dates,fields='ts_code,end_date,eps,extra_item,gross_margin,current_ratio,quick_ratio,cash_ratio,invturn_days,arturn_days,inv_turn,ar_turn,ca_turn,fa_turn,op_income,daa,ebit,ebitda,fcff,fcfe,interestdebt,netdebt,working_capital,networking_capital,invest_capital,retained_earnings,bps,ocfps,cfps,ebit_ps,fcff_ps,fcfe_ps,netprofit_margin,grossprofit_margin,profit_to_gr,gc_of_gr,op_of_gr,ebit_of_gr,roe,roe_waa,roe_dt,roa,npta,roic,roe_yearly,roa2_yearly,roe_avg,dtprofit_to_profit,debt_to_assets,dp_assets_to_eqt,ocf_to_shortdebt,debt_to_eqt,ebit_to_interest,roa_yearly,roa_dp,profit_prefin_exp,roic_yearly,total_fa_trun,profit_to_op,basic_eps_yoy,cfps_yoy,op_yoy,ebt_yoy,netprofit_yoy,dt_netprofit_yoy,ocf_yoy,roe_yoy,bps_yoy,assets_yoy,eqt_yoy,or_yoy')
    appended_data.append(all_data)
appended_data = pd.concat(appended_data)

#Export the df to excel
appended_data.to_excel(r'C:\Users\Austin\Desktop\Tushare\list3.xlsx', index = False)


