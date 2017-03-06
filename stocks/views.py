from django.http import HttpResponse
from django.db.models import Max
from models import StockIndex, Stock, DailyPrice
from utils import normalize_string
from time import mktime
import json

def JsonResponse(data):
    return HttpResponse(json.dumps(data), content_type="application/json")

def JsonSuccess(message):
    response_data = {}
    response_data['success'] = True
    response_data['message'] = message
    return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

def JsonError(message):
    response_data = {}
    response_data['success'] = False
    response_data['message'] = message
    return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

def index(request):
    return JsonSuccess("This is the stocks index. Try to use any other apis instead")

def get_stock(request, stock_code):
    try:
        result = Stock.objects.get(stock_code=normalize_string(stock_code))

        response_data = {}
        response_data["stock_code"] = result.stock_code
        response_data["url"] = result.url
        response_data["index"] = result.listed_index.index_code

        # daily prices
        prices = list(result.dailyprice_set.order_by('-close_date').only('close_date','close_price','oscillate')[:5])
        response_prices = []

        for price in prices:
            entry = {}
            entry["close_date"] = int(mktime(price.close_date.timetuple())*1000)
            entry["close_price"] = price.close_price
            entry["oscillate"] = price.oscillate
            response_prices.append(entry)

        response_data["prices"] = response_prices

        return JsonResponse(response_data)
    except Stock.DoesNotExist:
        return JsonError("Stock does not exist")

def find_stock(request, code, limit="5"):
    try:
        limit = min(int(limit), 5)
        results = Stock.objects.filter(stock_code__startswith=normalize_string(code))[:limit]
        response_data = []

        for result in results:
            response_item = {}
            response_item["stock_code"] = result.stock_code
            response_item["url"] = result.url
            response_item["index"] = result.listed_index.index_code
            response_data.append(response_item)

        return JsonResponse(response_data)
    except Stock.DoesNotExist:
        return JsonError("Stock does not exist")

def top_stocks(request, timestamp=0, limit="10"):
    try:
        if timestamp == 0:
            #try to get latest time
            max_date = DailyPrice.objects.all().aggregate(Max('close_date'))['close_date__max']
        else:
            max_date = timestamp
        results = DailyPrice.objects.filter(close_date__date=max_date.date()).order_by('-oscillate_percent')[:10]
        response_data = []

        for result in results:
            response_item = {}
            response_item["stock_code"] = result.stock_code
            response_item["url"] = result.url
            response_item["index"] = result.listed_index.index_code
            response_data.append(response_item)

        return JsonResponse(response_data)
    except DailyPrice.DoesNotExist:
        return JsonError("Stock does not exist")
