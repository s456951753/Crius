import Utils.numeric_utils as TuRq
from datetime import datetime, timedelta
import time as t
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import talib


list = ['000685.SZ', '000690.SZ', '000935.SZ', '000937.SZ', '002004.SZ', '002048.SZ',
        '002419.SZ', '002430.SZ', '002440.SZ', '002444.SZ', '002531.SZ', '002597.SZ',
        '002605.SZ', '002798.SZ', '300080.SZ', '300118.SZ', '600064.SH', '600295.SH', '600329.SH',
        '600348.SH', '600507.SH', '600682.SH', '600717.SH', '600729.SH', '600803.SH', '601107.SH',
        '601163.SH', '601330.SH', '601567.SH', '603328.SH']


all_data = []
# 遍历list里面的股票，可以写入多个股票
for ticker in list:
    # 获取各股票某时段的价格
    all_data[ticker] = TuRq.get_converted_stock_code(ticker)
    all_data.append(ticker.strip())

print(all_data)