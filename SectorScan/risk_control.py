## 个股止损
def security_stoploss(context,loss=0.1):
    if len(context.portfolio.positions)>0:
        for stock in context.portfolio.positions.keys():
            avg_cost = context.portfolio.positions[stock].avg_cost
            current_price = context.portfolio.positions[stock].price
            if 1 - current_price/avg_cost >= loss:
                log.info(str(stock) + '  跌幅达个股止损线，平仓止损！')
                order_target_value(stock, 0)

## 个股止盈
def security_stopprofit(context,profit=0.1):
    if len(context.portfolio.positions)>0:
        for stock in context.portfolio.positions.keys():
            avg_cost = context.portfolio.positions[stock].avg_cost
            current_price = context.portfolio.positions[stock].price
            if current_price/avg_cost - 1 >= profit:
                log.info(str(stock) + '  涨幅达个股止盈线，平仓止盈！')
                order_target_value(stock, 0)

## 大盘止损
# 止损方法1：根据大盘指数N日均线进行止损
def index_stoploss_sicha(index, context, n=60):
    '''
    当大盘N日均线(默认60日)与昨日收盘价构成“死叉”，则清仓止损
    '''
    if len(context.portfolio.positions)>0:
        hist = attribute_history(index, n+2, '1d', 'close', df=False)
        temp1 = mean(hist['close'][1:-1])
        temp2 = mean(hist['close'][0:-2])
        close1 = hist['close'][-1]
        close2 = hist['close'][-2]
        if (close2 > temp2) and (close1 < temp1):
            log.info('大盘触及止损线，清仓！')
            for stock in context.portfolio.positions.keys():
                order_target_value(stock, 0)
# 止损方法2：根据大盘指数跌幅进行止损
def index_stoploss_diefu(index, context, n=10, zs=0.03):
    '''
    当大盘N日内跌幅超过zs，则清仓止损
    '''
    if len(context.portfolio.positions)>0:
        hist = attribute_history(index, n, '1d', 'close',df=False)
        if ((1-float(hist['close'][-1]/hist['close'][0])) >= zs):
            log.info('大盘触及止损线，清仓！')
            for stock in context.portfolio.positions.keys():
                order_target_value(stock, 0)