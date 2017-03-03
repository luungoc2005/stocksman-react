from datetime import date, timedelta, datetime
from urllib import urlopen
from time import sleep
from pytz import utc

from stocks.utils import normalize_string, price_from_json
from stocks.models import DailyPrice, Stock, ErrorLog

STOCKS_LINK = "http://finance.vietstock.vn/AjaxData/TradingResult/GetStockData.ashx?scode={1}"

def get_latest_weekday():
    today_date = date.today()
    weekday = today_date.weekday()
    if weekday >= 5:
        today_date = today_date - timedelta(days=(6-weekday))
    return today_date

def geturl(url):
    "Get text content from url"
    content = urlopen(url)
    return content.read()

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
