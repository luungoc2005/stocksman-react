from __future__ import unicode_literals

from django.db import models

# Create your models here.
class StockIndex(models.Model):
    "Object containing all stocks listed on an index"
    index_code = models.CharField(max_length=10)

class Stock(models.Model):
    "Object containing daily prices of a stock. To add groups later"
    stock_code = models.CharField(max_length=5)
    listed_index = models.ForeignKey(StockIndex, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)

class DailyPrice(models.Model):
    "Daily price containing all information"
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, db_index=True)
    "Price fields"
    close_date = models.DateTimeField('Close Date', db_index=True)
    open_price = models.IntegerField(default=0)
    close_price = models.IntegerField(default=0)
    avg_price = models.IntegerField(default=0)
    floor_price = models.IntegerField(default=0)
    ceiling_price = models.IntegerField(default=0)
    highest = models.IntegerField(default=0)
    lowest = models.IntegerField(default=0)
    oscillate = models.IntegerField(default=0)
    "Other integer fields"
    dividend = models.IntegerField(default=0)
    eps = models.IntegerField(default=0)
    buy_redundancy = models.IntegerField(default=0)
    sell_redundancy = models.IntegerField(default=0)
    bvps = models.IntegerField(default=0)
    capital_level = models.IntegerField(default=0)
    curr_room = models.IntegerField(default=0)
    klcplh = models.BigIntegerField(default=0)
    klcpny = models.BigIntegerField(default=0)
    "Volume"
    avg_vol = models.IntegerField(default=0)
    trading_vol = models.BigIntegerField(default=0)
    total_vol = models.BigIntegerField(default=0)
    "Decimals"
    beta = models.DecimalField(max_digits=10, decimal_places=5)
    dec_pb = models.DecimalField(max_digits=20, decimal_places=10)
    dec_pe = models.DecimalField(max_digits=20, decimal_places=10)
    fw_pe = models.DecimalField(max_digits=20, decimal_places=10)
    "Raw data"
    raw_json = models.CharField(max_length=1024)

    def oscillate_percent(self):
        "Returns oscillate as percentage"
        if self.close_price == 0:
            return 0
        else:
            return self.oscillate / self.close_price

class ErrorLog(models.Model):
    date = models.DateTimeField('Date')
    dest_url = models.CharField(max_length=500)
    raw_json = models.CharField(max_length=1024)