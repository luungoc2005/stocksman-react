from django.http import HttpResponse
from django.db.models import Max

from .models import StockIndex, Stock, DailyPrice
from .utils import normalize_string

from datetime import datetime, timedelta
from time import mktime

from .learn import predict_stock

import json

def JsonResponse(data):
    return HttpResponse(json.dumps(data), content_type='application/json')

def JsonSuccess(message):
    response_data = {}
    response_data['success'] = True
    response_data['message'] = message
    return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)

def JsonError(message):
    response_data = {}
    response_data['success'] = False
    response_data['message'] = message
    return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

def index(request):
    return JsonSuccess('This is the stocks index. Try to use any other apis instead')

def get_indices(request):
    result = list(StockIndex.objects.all())
    response_data = [obj.index_code for obj in result]
    return JsonResponse(response_data)

def get_stock(request, stock_code):
    try:
        result = Stock.objects.get(stock_code=normalize_string(stock_code))

        response_data = {}
        response_data['stock_code'] = result.stock_code
        response_data['url'] = result.url
        response_data['index'] = result.listed_index.index_code

        # daily prices
        prices = list(result.dailyprice_set.order_by('-close_date').only('close_date','close_price','oscillate')[:5])
        response_prices = []

        for price in prices:
            entry = {}
            entry['close_date'] = int(mktime(price.close_date.timetuple())*1000)
            entry['close_price'] = price.close_price
            # entry['close_price_t3'] = price.close_price_t3 # for testing T+3
            entry['oscillate'] = price.oscillate
            entry['oscillate_percent'] = price.oscillate_percent
            response_prices.append(entry)

        response_data['prices'] = response_prices

        return JsonResponse(response_data)
    except Stock.DoesNotExist:
        return JsonError('Stock does not exist')

def find_stock(request, code, limit='5'):
    try:
        limit = min(int(limit), 5)
        results = Stock.objects.filter(stock_code__startswith=normalize_string(code))[:limit]
        response_data = []

        for result in results:
            response_item = {}
            response_item['stock_code'] = result.stock_code
            response_item['url'] = result.url
            response_item['index'] = result.listed_index.index_code
            response_data.append(response_item)

        return JsonResponse(response_data)
    except Stock.DoesNotExist:
        return JsonError('Stock does not exist')

def top_stocks(request, filter='', timestamp=0, limit='7', t3=False):
    try:
        if limit == None:
            limit = 7
        limit = min(int(limit), 7)
        if timestamp == None or int(timestamp) == 0:
            #try to get latest time
            max_date = DailyPrice.objects.all().aggregate(Max('close_date'))['close_date__max']
            if t3 == True:
                num_days = 3
                for i in range(3,6):
                    min_weekday = (max_date - timedelta(days=num_days)).weekday()
                    if min_weekday == 5 or min_weekday == 6:
                        num_days = i
                    else:
                        break
                max_date = max_date - timedelta(days=num_days)
        else:
            max_date = datetime.fromtimestamp(int(timestamp))
        results = DailyPrice.objects.filter(close_date__date=max_date.date()).only('stock','close_date','close_price','oscillate')

        if filter != None and filter != '':
            results = results.filter(stock__listed_index__index_code=normalize_string(filter))
        
        if t3 == True:
            results = sorted(results.all(), key=lambda x: x.oscillate_percent_t3,
                            reverse=True)[:limit]
        else:
            results = sorted(results.all(), key=lambda x: x.oscillate_percent,
                            reverse=True)[:limit]
        response_data = []

        for result in results:
            response_stock = result.stock
            response_item = {}
            response_item['stock_code'] = response_stock.stock_code
            response_item['url'] = response_stock.url
            response_item['index_code'] = response_stock.listed_index.index_code
            response_item['close_date'] = int(mktime(result.close_date.timetuple())*1000)

            if t3 == True:
                response_item['close_price'] = result.close_price_t3
                response_item['oscillate'] = result.oscillate_t3
                response_item['oscillate_percent'] = result.oscillate_percent_t3
            else:
                response_item['close_price'] = result.close_price
                response_item['oscillate'] = result.oscillate
                response_item['oscillate_percent'] = result.oscillate_percent

            response_data.append(response_item)

        return JsonResponse(response_data)
    except DailyPrice.DoesNotExist:
        return JsonError('Stock does not exist')

def project_stock(request, stock_code):
    price, cls_prob, reg, adj = predict_stock(stock_code)

    response_data = {}
    response_data['stock_code'] = stock_code
    response_data['prob_negative'] = cls_prob[0][0]
    response_data['prob_positive'] = cls_prob[0][1]
    response_data['future_price'] = int(round((1 + reg[0]) * price, 0))
    response_data['adj_price'] = int(round((1 + adj[0]) * price, 0))

    return JsonResponse(response_data)
