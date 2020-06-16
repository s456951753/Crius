import rqalpha.portfolio
import rqalpha.model.order
import time
from rqalpha.const import ORDER_STATUS


def get_info_for_order(order: rqalpha.model.order, portfolio: rqalpha.portfolio, logger, logging_level="info"):
    breaker = 0
    while (not order.is_final() and breaker < 5):
        logger.debug("order is not finalized. Sleeping for 1 sec")
        time.sleep(1)
        breaker = breaker + 1
    if (breaker == 5):
        logger.error("order not finalized in 5 seconds. your script might have stuck")
    logger.info(
        order.datetime() + " order " + order.order_id() + " exercised. " + order.order_book_id() + " fulfilled" + order.filled_quantity() + " at " + order.avg_price())
    logger.info(
        "current cash level" + portfolio.cash() + ". " + "total value is " + portfolio.total_value() + ". total return by today is " + portfolio.total_returns())
    if (logging_level == "info"):
        pass
    logger.debug("detailed info for" + order.order_id() + ": ")
    if (order.price() == 0):
        logger.debug("placed: " + order.quantity() + " of " + order.order_book_id())
    else:
        logger.debug("placed: " + order.quantity() + " at " + order.price())
    logger.debug("fulfilled: " + order.filled_quantity() + " at " + order.avg_price())
    logger.debug("current positions:")
    logger.debug(portfolio.positions)
