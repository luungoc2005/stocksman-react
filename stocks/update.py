from time import sleep
from datetime import datetime
from pytz import utc

from stocks.utils import normalize_string, price_from_json, geturl, get_latest_weekday
from stocks.models import DailyPrice, Stock, ErrorLog

STOCKS_LINK = "http://finance.vietstock.vn/AjaxData/TradingResult/GetStockData.ashx?scode={1}"

def try_add(url, max_tries=3):
    for attempt in range(1, max_tries):
        try:
            raw_data = geturl(url)
            price_from_json(raw_data)
            break
        except:
            new_log = ErrorLog(date=datetime.now(utc), dest_url=url, raw_json=raw_data)
            new_log.save()
            print "Retrying after 5s - remaining tries: " + str(max_tries - attempt)
            sleep(5)

def update_stock(stock_code):
    today_date = get_latest_weekday()
    price_query = DailyPrice.objects.filter(stock__stock_code=normalize_string(stock_code), close_date__date=today_date)
    if (price_query.exists() != True):
        print "Updating " + stock_code
        try_add(STOCKS_LINK.replace("{1}", stock_code))

def update_all():
    stocks_list = list(Stock.objects.all().only('stock_code'))
    for stock in stocks_list:
        update_stock(stock.stock_code)
