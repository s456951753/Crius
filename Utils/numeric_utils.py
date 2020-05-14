# DONE: #请define 一个新功能来转化Tushare 和 Rqalpha 的股票代码。 一个功能是 Tushare 转 Rqalpha 另一个是 Rqalpha 转 Tushare

# DONE:Tushare 的股票代码格式 举例： 000690.SZ （深市）or 603328.SH （沪市）

# DONE:Rqalpha 的股票代码格式 举例： 000690.XSHE （深市）or 603328.XSHG （沪市）

import re


def get_converted_stock_code(symbol):
    validate(symbol)
    symbol = str(symbol)
    new_symbol = symbol.split('.')
    dic = {'SZ': 'XSHE',
           'SH': 'XSHG',
           'XSHE': 'SZ',
           'XSHG': 'SH'}
    return new_symbol[0] + '.' + dic.get(new_symbol[1])


def validate(symbol):
    a = re.compile("\d{6}\.SZ|SH|XSHE|XSHG")
    if (a.search(symbol) == None):
        raise NameInvalidException(symbol)


class NameInvalidException(Exception):
    def __init__(self, symbol):
        self.symbol = symbol
        self.message = symbol + " is not a valid symbol"
