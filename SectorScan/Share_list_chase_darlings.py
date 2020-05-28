import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Load Tushare
import Utils.configuration_file_service as config_service
import tushare as ts

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)

#基金持股快照

#日期格式为 月/日/年
start_date = '4/1/2020'
end_date = '7/1/2020'

datelist = pd.date_range(start=start_date, end=end_date)
date_strings = [datetime.strftime(d, '%Y%m%d') for d in datelist]

fund_list = pd.read_excel (r'C:\Users\Austin\Desktop\Tushare\Tushare_Fund_data.xlsx', index = False)


fund_list_snapshot = fund_list[fund_list.end_date.isin(date_strings)]

fund_list_snapshot = pd.pivot_table(fund_list_snapshot,index=["symbol"],aggfunc={'stk_mkv_ratio':np.sum,'ts_code':np.count_nonzero,'mkv':np.sum,'amount':np.sum})

fund_list_snapshot = fund_list_snapshot.sort_values(by='stk_mkv_ratio', ascending=False)

print(fund_list_snapshot)
#Export the df to excel
fund_list_snapshot.to_excel(r'C:\Users\Austin\Desktop\Tushare\list3.xlsx', index = True)