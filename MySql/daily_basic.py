# -*- coding: utf-8 -*-

#Load Tushare

import Utils.configuration_file_service as config_service
import tushare as ts
import time

token = config_service.getProperty(section_name=config_service.TOKEN_SECTION_NAME,
                                   property_name=config_service.TS_TOKEN_NAME)
pro = ts.pro_api(token)

# 1.创建表结构
from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DailyBasic(Base):
    """股票列表
    ts_code	str	Y	股票代码（二选一）
    trade_date	str	N	交易日期 （二选一）
    start_date	str	N	开始日期(YYYYMMDD)
    end_date	str	N	结束日期(YYYYMMDD)
    """
    __tablename__ = 'daily_basic'

    ts_code = Column(String(10), primary_key=True)  # TS代码
    trade_date = Column(String(8), primary_key=True)# 交易日期
    close = Column(float)                           # 当日收盘价
    turnover_rate = Column(float)                   # 换手率（%）
    turnover_rate_f = Column(float)                 # 换手率（自由流通股）
    volume_ratio = Column(float)                    # 量比
    pe = Column(float)                              # 市盈率（总市值/净利润， 亏损的PE为空）
    pe_ttm = Column(float)                          # 市盈率（TTM，亏损的PE为空）
    pb = Column(float)                              # 市净率（总市值/净资产）
    ps = Column(float)                              # 市销率
    ps_ttm = Column(float)                          # 市销率（TTM）
    dv_ratio = Column(float)                        # 股息率 （%）
    dv_ttm = Column(float)                          # 股息率（TTM）（%）
    total_share = Column(float)                     # 总股本 （万股）
    float_share = Column(float)                     # 流通股本 （万股）
    free_share = Column(float)                      # 自由流通股本 （万）
    total_mv = Column(float)                        # 总市值 （万元）
    circ_mv = Column(float)                         # 流通市值（万元）

# 2. 建立获取tushare数据函数

trade_date_list = ['19911228','19911229','19911230','19911231']

from sqlalchemy import create_engine

def get_daily_basic(pro, retry_count=3, pause=2):
    """数据"""
    frame = pd.DataFrame()
    for date in trade_date_list:
        for _ in range(retry_count):
            try:
                df = pro.daily_basic(ts_code='', trade_date=date, fields='ts_code, trade_date, close, turnover_rate, \
                turnover_rate_f, volume_ratio, pe, pe_ttm, pb, ps, ps_ttm, dv_ratio, dv_ttm, total_share, \
                float_share, free_share, total_mv, circ_mv')
            except:
                time.sleep(pause)
            else:
                frame = frame.append(df)
                break

    return frame


# 3. 更新数据

import pandas as pd

def truncate_update(engine, data, table_name):
    """删除mysql表所有数据，to_sql追加新数据"""
    conn = engine.connect()
    conn.execute('truncate ' + table_name)
    data.to_sql(table_name, engine, if_exists='append', index=False)


def update_daily_basic(engine, pro, retry_count, pause):
    """更新 所有数据"""
    data = get_daily_basic(pro, retry_count, pause)
    truncate_update(engine, data, 'daily_basic')

# 4. 主程序

# 创建数据库引擎
engine = create_engine(config_service.getDefaultDB())
conn = engine.connect()

# 创建mysql所有表结构
Base.metadata.create_all(engine)

# 列表
update_daily_basic(engine, pro, 3, 2)
