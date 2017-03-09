from .models import StockIndex, Stock, DailyPrice
from .utils import normalize_string

from random import shuffle
from datetime import datetime, timedelta
from operator import itemgetter

from django.db.models import Max
from django.forms.models import model_to_dict

from sklearn import preprocessing, model_selection, neural_network
import numpy

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
    ret_list.extend([price.variation, price.oscillate_percent, price.moving_average])
    return ret_list

def get_output_value(price):
    return float(price.oscillate_t3 > 0)

def get_eval_data():
    global X_train
    global X_test
    global y_train
    global y_test

    lookup_date = DailyPrice.objects.all().aggregate(Max('close_date'))['close_date__max'] - timedelta(days=MIN_DAYS)
    results = list(DailyPrice.objects.filter(close_date__gte=lookup_date).defer('close_date', 'stock', 'raw_json'))
    results = [o for o in results if o != None and o.close_price_t3 > 0 and o.moving_average > 0]
    print('Length: ' + str(len(results)))
    # shuffle(results)

    inputs = numpy.array([get_input_array(o) for o in results], dtype='f8')
    outputs = numpy.array([get_output_value(o) for o in results], dtype='f8')

    inputs_scaled = preprocessing.scale(inputs)
    # outputs_scaled = preprocessing.scale(outputs)

    print(inputs_scaled)
    # print(outputs_scaled)
    print(outputs)

    return model_selection.train_test_split(inputs_scaled, outputs, test_size=0.2)
    # clf=neural_network.MLPRegressor(activation='relu', alpha=1e-05, batch_size='auto',
    #                                 beta_1=0.9, beta_2=0.999, early_stopping=True,
    #                                 epsilon=1e-08, hidden_layer_sizes=(100, 50), learning_rate='adaptive',
    #                                 learning_rate_init=0.001, max_iter=50000, momentum=0.9,
    #                                 nesterovs_momentum=True, power_t=0.5, random_state=None, shuffle=True,
    #                                 solver='adam', tol=0.000001, validation_fraction=0.1, verbose=True,
    #                                 warm_start=False) # Best: Accuracy: 0.0768774481639
    # clf=neighbors.KNeighborsRegressor(n_neighbors=10, weights='distance', algorithm='auto',
    #                                     leaf_size=30, p=2, metric='minkowski',
    #                                     metric_params=None, n_jobs=1)
    # clf=tree.DecisionTreeRegressor(criterion='mse', splitter='best', max_depth=None,
    #                                 min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0,
    #                                 max_features=None, random_state=None, max_leaf_nodes=None,
    #                                 min_impurity_split=1e-07, presort=False)
    # clf=kernel_ridge.KernelRidge(alpha=1.0, coef0=1, degree=3, gamma=None, kernel='linear',
    #         kernel_params=None)

    # clf_array = []
    # accuracy_array = []
    # for i in range(3,25):
    #     clf=neighbors.KNeighborsRegressor(n_neighbors=i, weights='distance', algorithm='auto',
    #                                 leaf_size=30, p=2, metric='minkowski',
    #                                 metric_params=None, n_jobs=1)
    #     clf.fit(X_train, y_train)
    #     accuracy = clf.score(X_test, y_test)
    #     print(str(i) + ' neighbors - Accuracy: ' + str(accuracy))

    #     clf_array.append(clf)
    #     accuracy_array.append(abs(accuracy))

    # index, value = max(enumerate(accuracy_array), key=itemgetter(1))
    # print('Best: ' + str(index + 3) + ' - Accuracy: ' + str(value))