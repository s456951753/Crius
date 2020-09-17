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

import mysql.connector as mysql

mydb = mysql.connect(
        host="127.0.0.1",
        user="root",
        passwd="3c311a",
       database="crius_sql")

def deleteDuplicates():
    stop = False
    while (not stop):
        mycursor = mydb.cursor()
        get_dup_query = "select id from (select min(x.id) as id,x.ts_code,x.trade_date from (SELECT id,new_daily_2015_2019.ts_code as ts_code,new_daily_2015_2019.trade_date as trade_date FROM new_daily_2015_2019 INNER JOIN (SELECT trade_date,ts_code FROM new_daily_2015_2019 GROUP BY trade_date,ts_code HAVING COUNT(id) > 1) dup ON new_daily_2015_2019.trade_date = dup.trade_date and new_daily_2015_2019.ts_code = dup.ts_code)x GROUP BY x.trade_date,x.ts_code)y;"
        mycursor.execute(get_dup_query)
        databaseIds = mycursor.fetchall()
        print("Total rows are:  ", len(databaseIds))
        if len(databaseIds) == 0:
            stop = True
        for id in databaseIds:
            id_value = id[0]
            delete_query = "DELETE FROM new_daily_2015_2019 WHERE id = '{0}';".format(id_value)
            # print("id : ",id[0])
            mycursor.execute(delete_query)
            print(delete_query)
        mycursor.close()
        mydb.commit()

    print("Process complete!!!")



def main():
    deleteDuplicates()


if __name__ == "__main__":
    main()
