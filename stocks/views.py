from django.http import HttpResponse
from models import StockIndex, Stock, DailyPrice
from utils import normalize_string
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

        return JsonResponse(response_data)
    except Stock.DoesNotExist:
        return JsonError("Stock does not exist")

def find_stock(request, code, limit="10"):
    try:
        limit = min(int(limit), 10)
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
