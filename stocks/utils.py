from models import Stock, DailyPrice
import json

def normalize_string(input):
    return input.strip().upper()

def price_from_json(json_data):
    "Gets daily price model from json data"
    parsed_data = json.load(json_data, encoding='utf-8')
    stock_model = Stock.objects.get(stock_code=normalize_string(parsed_data['StockCode']))
    stock_model.dailyprice_set.create(
        "Price fields"
        close_date = parsed_data["CloseDate"],
        open_price = models.IntegerField(default=0),
        close_price = models.IntegerField(default=0),
        avg_price = models.IntegerField(default=0),
        floor_price = models.IntegerField(default=0),
        ceiling_price = models.IntegerField(default=0),
        highest = models.IntegerField(default=0),
        lowest = models.IntegerField(default=0),
        oscillate = models.IntegerField(default=0),
        "Other integer fields"
        dividend = models.IntegerField(default=0),
        eps = models.IntegerField(default=0),
        buy_redundancy = models.IntegerField(default=0),
        sell_redundancy = models.IntegerField(default=0),
        bvps = models.IntegerField(default=0),
        capital_level = models.IntegerField(default=0),
        curr_room = models.IntegerField(default=0),
        klcplh = models.BigIntegerField(default=0),
        klcpny = models.BigIntegerField(default=0),
        "Volume"
        avg_vol = models.IntegerField(default=0),
        trading_vol = models.BigIntegerField(default=0),
        total_vol = models.BigIntegerField(default=0),
        "Decimals"
        beta = models.DecimalField(max_digits=10, decimal_places=5),
        dec_pb = models.DecimalField(max_digits=20, decimal_places=10),
        dec_pe = models.DecimalField(max_digits=20, decimal_places=10),
        fw_pe = models.DecimalField(max_digits=20, decimal_places=10),
        "Raw data"
        raw_json = models.CharField(max_length=1024),
    )