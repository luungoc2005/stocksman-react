from .models import Stock, DailyPrice
from django.db.models import Max

from datetime import datetime, date, timedelta
from pytz import timezone
from time import mktime

from os import listdir
from os.path import join, abspath, dirname
from uuid import uuid4

from urllib import request
from bs4 import BeautifulSoup
import codecs
import json

APP_ROOT = dirname(abspath(__file__))

def random_file_name(path = '', prefix = ''):
    return join(APP_ROOT, path, 
            prefix + str(int(mktime(datetime.utcnow().timetuple()))) + '-' \
                    + str(uuid4()))

def get_latest_weekday(input_date=None):
    if input_date == None:
        find_date = date.today()
    else:
        find_date = input_date
    weekday = find_date.weekday()
    if weekday >= 5:
        today_date = find_date - timedelta(days=(6-weekday))
    return find_date

def geturl(url):
    'Get text content from url'
    content = request.urlopen(url)
    return content.read()

def readfile(filename):
    'Read file and return as string'
    with codecs.open(filename, 'r', 'utf-8-sig') as target:
        return target.read()

def readfile_lines(filename):
    'Read file and return as list of lines'
    with codecs.open(filename, 'r', 'utf-8-sig') as target:
        return target.readlines()

def normalize_string(input):
    return input.strip().upper()

def parse_date(obj):
    if 'CloseDate' in obj:
        timestamp = int(obj['CloseDate'][6:-2]) / 1000
        obj['CloseDate'] = datetime.fromtimestamp(timestamp, tz=timezone('Asia/Ho_Chi_Minh'))
    return obj

def price_from_json(json_data):
    'Gets daily price model from json data'
    # Set new daily price data
    # parsed_data = list(json.loads(json_data, encoding='utf-8'))[0]
    parsed_data = list(json.loads(json_data, encoding='utf-8', object_hook=parse_date))[0]
    stock_model = Stock.objects.get(stock_code=normalize_string(parsed_data['StockCode']))
    # Map new price
    new_price = DailyPrice()
    new_price.stock = stock_model
    # Price fields
    new_price.close_date = parsed_data['CloseDate']
    new_price.open_price = parsed_data['OpenPrice']
    new_price.close_price = parsed_data['ClosePrice']
    new_price.avg_price = parsed_data['AvrPrice']
    new_price.floor_price = parsed_data['FloorPrice']
    new_price.ceiling_price = parsed_data['CeilingPrice']
    new_price.highest = parsed_data['Highest']
    new_price.lowest = parsed_data['Lowest']
    new_price.oscillate = parsed_data['Oscillate']
    # Other integer fields
    new_price.dividend = parsed_data['Dividend']
    new_price.eps = parsed_data['EPS']
    new_price.buy_redundancy = parsed_data['BuyRedundancy']
    new_price.sell_redundancy = parsed_data['SellRedundancy']
    new_price.bvps = parsed_data['BVPS']
    new_price.capital_level = parsed_data['CapitalLevel']
    new_price.curr_room = parsed_data['CurrRoom']
    new_price.klcplh = parsed_data['KLCPLH']
    new_price.klcpny = parsed_data['KLCPNY']
    # Volume
    new_price.avg_vol = parsed_data['AvgVol']
    new_price.trading_vol = parsed_data['TradingVolume']
    new_price.total_vol = parsed_data['TotalVal']
    # Decimals
    new_price.beta = parsed_data['Beta']
    new_price.dec_pb = parsed_data['PB']
    new_price.dec_pe = parsed_data['PE']
    new_price.fw_pe = parsed_data['FwPE']
    # Raw data
    new_price.raw_json = json_data
    # Set URL to Stock model
    stock_model.url = parsed_data['URL']
    # save to Db
    new_price.save()
    stock_model.save()

def import_from_directory(dirname):
    'Batch import from directory'
    file_list = listdir(dirname)
    for file_name in file_list:
        full_path = join(dirname, file_name)
        lines_list = list(readfile_lines(full_path))
        print('Importing ' + str(len(lines_list)) + ' from ' + file_name)
        for line_string in lines_list:
            line_string = line_string.strip()
            if line_string != '':                
                try:
                    price_from_json(line_string)
                except:
                    print('Error at ' + line_string + ' in ' + full_path)

def find_company_names():
    queryset = Stock.objects.all().only('company_name', 'url', 'stock_code')
    for item in list(queryset):
        if (item.company_name == '') and (item.url != ''):
            try:
                print('Getting company name for %s' % item.stock_code)
                content = request.urlopen(item.url)
                soup = BeautifulSoup(content, 'lxml')
                item.company_name = soup.find(
                    'td', {'class':'Finance_CompanyName'}).find(
                    'h1').find(
                    text=True, recursive=False).strip()
                item.save()
            except:
                print('Error encountered')

def find_industry():
    queryset = Stock.objects.all().only('stock_code', 'industry')
    count = Stock.objects.all().aggregate(Max('industry'))['industry__max'] + 1
    print('Max_industry: %s' % str(count))
    for item in list(queryset):
        if item.industry == 0:
            print('Getting industry for %s' % item.stock_code)

            response = request.urlopen(r'http://finance.vietstock.vn/Controls/TradingResult/Company_InSameIndustry_FilterProcess.ashx?Goals=all&Condition=than&val1=0&val2=100&Goals2=Price&Condition2=than&val21=0&val22=100&Goals3=Price&Condition3=than&val31=0&val32=100&countF=1&scode=' + item.stock_code + r'&fdate=03%2F15%2F17&catID=-1&sort=MktCap&dir=desc&page=1&psize=10&typeDo=filter')
            data = json.loads(response.read(), encoding='utf-8')
            industry_list = list(data['data'][0]['InSameIndustry'])
            print('Found %s stocks in the same industry' % str(len(industry_list)))
            set_industry = False
            for tag in industry_list:
                code=tag['StockCode']
                # print('Found stock in same industry: %s' % code)
                try:
                    item2 = Stock.objects.get(stock_code=normalize_string(code))
                except:
                    item2 = None
                if item2 != None:
                    if item2.industry == 0:
                        print('\tSetting industry for %s' % item2.stock_code)
                        item2.industry = count
                        item.industry = count
                        item.save()
                        item2.save()
                        set_industry = True
                    elif item2.industry != item.industry:
                        print('\tSetting back industry for %s' % item.stock_code)
                        item.industry = item2.industry
                        item.save()
            if set_industry == True:
                count += 1

def find_events():
    for price in list(DailyPrice.objects.all()):
        if price.is_event:
            print('Event: ' + price.stock.stock_code + ' on ' + str(price.close_date.date()) + ': ' \
            + str(price.previous_close_price) + ' -> ' + str(price.close_price))

def date_to_int(date):
    return int(mktime(date.timetuple())*1000)