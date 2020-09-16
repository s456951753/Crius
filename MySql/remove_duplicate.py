"""
Refactored so more suitable for sharded daily qfq data table
"""
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

engine = create_engine(config_service.getDefaultDB())
conn = engine.connect()

logger = logging.getLogger('daily_sharded')
logger.setLevel(logging.DEBUG)

import mysql.connector as mysql

mydb = mysql.connect(
        host="127.0.0.1",
        user="root",
        passwd="3c311a",
       database="crius_sql")

def deleteDuplicates():
    mycursor = mydb.cursor()
    get_dup_query = "select id from (select min(x.id) as id,x.ts_code,x.trade_date from (SELECT id,new_daily_2015_2019.ts_code as ts_code,new_daily_2015_2019.trade_date as trade_date FROM new_daily_2015_2019 INNER JOIN (SELECT trade_date,ts_code FROM new_daily_2015_2019 GROUP BY trade_date,ts_code HAVING COUNT(id) > 1) dup ON new_daily_2015_2019.trade_date = dup.trade_date and new_daily_2015_2019.ts_code = dup.ts_code)x GROUP BY x.trade_date,x.ts_code)y;"
    mycursor.execute(get_dup_query)
    logger.debug("get_dup_query_executed")
    databaseIds = mycursor.fetchall()
    logger.debug("fetchall")
    for id in databaseIds:
        id_value = id[0]
        delete_query = "DELETE FROM new_daily_2015_2019 WHERE id = '{0}';".format(id_value)
        #print("id : ",id[0])
        mycursor.execute(delete_query)
        print(delete_query)
    mycursor.close()
    logger.debug("mycursor_close")
    mydb.commit()
    logger.debug("mydb_commit")


def main():
    deleteDuplicates()


if __name__ == "__main__":
    main()
