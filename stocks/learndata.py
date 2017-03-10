from .models import StockIndex, Stock, DailyPrice, Scaler
from .utils import normalize_string

from random import shuffle
from datetime import datetime, timedelta
from operator import itemgetter

from django.db.models import Max
from django.forms.models import model_to_dict

from sklearn import preprocessing, model_selection, neural_network
import numpy
import pickle

MIN_DAYS = 60

def get_input_array(price):
    ret_list = [float(o) for o in list(model_to_dict(price,
        fields=['close_price', 'open_price', 'avg_price', 'oscillate',
                'dividend', 'eps', 'beta']).values())]
                # 'bvps', 'capital_level', 'curr_room', 'klcplh', 'klcpny',
                # 'total_vol', 'trading_vol',
                # 'dec_pb', 'dec_pe', 'fw_pe'
                # 'buy_redundancy', 'sell_redundancy',
    ret_list.extend([float(o == price.weekday) for o in range(0,4)]) # weekday
    ret_list.extend([price.variation, price.oscillate_percent, price.moving_average, price.is_event])
    return ret_list

def get_output_class(price):
    return float(price.oscillate_t3 > 0)

def get_output_value(price):
    return float(price.oscillate_percent_t3)

def get_eval_data():
    lookup_date = DailyPrice.objects.all().aggregate(Max('close_date'))['close_date__max'] - timedelta(days=MIN_DAYS)
    results = list(DailyPrice.objects.filter(close_date__gte=lookup_date).defer('close_date', 'stock', 'raw_json'))
    results = [o for o in results if o != None and o.close_price_t3 > 0 and o.moving_average > 0]
    print('Length: ' + str(len(results)))
    # shuffle(results)

    inputs = numpy.array([get_input_array(o) for o in results], dtype='f8')
    outputs_cls = numpy.array([get_output_class(o) for o in results], dtype='f8')    
    outputs_reg = numpy.array([get_output_value(o) for o in results], dtype='f8')

    scaler = preprocessing.StandardScaler(
        copy=True, with_mean=True, with_std=True).fit(inputs)
    
    inputs_scaled = scaler.transform(inputs)
    
    scale_model = Scaler()
    scale_model.date = datetime.utcnow()
    scale_model.data = pickle.dumps(scaler)
    scale_model.save()

    # outputs_scaled = preprocessing.scale(outputs)

    print(inputs_scaled)
    # print(outputs_scaled)
    print(outputs_cls)
    print(outputs_reg)

    cls_data = model_selection.train_test_split(inputs_scaled, outputs_cls, test_size=0.2)
    reg_data = model_selection.train_test_split(inputs_scaled, outputs_reg, test_size=0.2)

    return scale_model, [cls_data, reg_data]