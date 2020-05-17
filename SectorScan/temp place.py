import Utils.numeric_utils as TuRq
from datetime import datetime, timedelta
import time as t
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import talib
import Utils.numeric_utils as TuRq


#list = ['000685.SZ', '000690.SZ', '000935.SZ', '000937.SZ', '002004.SZ', '002048.SZ',
#        '002419.SZ', '002430.SZ', '002440.SZ', '002444.SZ', '002531.SZ', '002597.SZ',
#        '002605.SZ', '002798.SZ', '300080.SZ', '300118.SZ', '600064.SH', '600295.SH', '600329.SH',
#        '600348.SH', '600507.SH', '600682.SH', '600717.SH', '600729.SH', '600803.SH', '601107.SH',
#        '601163.SH', '601330.SH', '601567.SH', '603328.SH']


#all_data = TuRq.get_list_of_converted_stock_code(list)

#print(all_data)

from datetime import date

today = date.today()

# dd/mm/YY
d1 = today.strftime("%Y%m%d")
print("d1 =", d1)
