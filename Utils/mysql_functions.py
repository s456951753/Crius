# coding=utf-8
#建立获取tushare数据函数，存为tushare_data.py

# coding=utf-8

import time
import pandas as pd


def get_stock_basic(pro, retry_count=3, pause=2):
    """股票列表 数据"""
    frame = pd.DataFrame()
    for status in ['L', 'D', 'P']:
        for _ in range(retry_count):
            try:
                df = pro.stock_basic(exchange='', list_status=status,
                                     fields='ts_code,symbol,name,area,industry,fullname,enname,market, \
                                    exchange,curr_type,list_status,list_date,delist_date,is_hs')
            except:
                time.sleep(pause)
            else:
                frame = frame.append(df)
                break

    return frame


#更新“股票列表”数据，存为mysql_functions.py

import pandas as pd
import tushare as ts

def truncate_update(engine, data, table_name):
    """删除mysql表所有数据，to_sql追加新数据"""
    conn = engine.connect()
    conn.execute('truncate ' + table_name)
    data.to_sql(table_name, engine, if_exists='append', index=False)


def update_stock_basic(engine, pro, retry_count, pause):
    """更新 股票信息 所有数据"""
    data = get_stock_basic(pro, retry_count, pause)
    truncate_update(engine, data, 'stock_basic')

