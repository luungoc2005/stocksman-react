from .learndata import *
from .utils import random_file_name

from sklearn import preprocessing, neural_network, neighbors, ensemble, svm, discriminant_analysis, kernel_ridge, tree
from datetime import datetime

from stocks.models import LearnModel, DailyPrice, Stock

import numpy
import pickle

CLASSIFIERS = [
    neural_network.MLPClassifier(hidden_layer_sizes=(30, 20), activation='sigmoid', solver='sgd', alpha=0.0001, batch_size='auto', learning_rate='adaptive', learning_rate_init=0.001, power_t=0.5, max_iter=50000, shuffle=True, random_state=None, tol=0.000001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08), #1

    neural_network.MLPClassifier(hidden_layer_sizes=(30, 20), activation='relu', solver='adam', alpha=0.0001, batch_size='auto', learning_rate='adaptive', learning_rate_init=0.001, power_t=0.5, max_iter=50000, shuffle=True, random_state=None, tol=0.000001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08), #2

    neighbors.KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=1), #3

    neighbors.KNeighborsClassifier(n_neighbors=5, weights='distance', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=1), #4

    ensemble.RandomForestClassifier(n_estimators=1000, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_split=1e-07, bootstrap=True, oob_score=False, n_jobs=-1, random_state=None, verbose=0, warm_start=False, class_weight=None), #5

    # svm.SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None, random_state=None), #6
    # svm.SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=True, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr', random_state=None), #6

    ensemble.AdaBoostClassifier(base_estimator=None, n_estimators=1000, learning_rate=1.0, algorithm='SAMME.R', random_state=None),
    ensemble.GradientBoostingClassifier(loss='deviance', learning_rate=0.1, n_estimators=100, subsample=1.0, criterion='friedman_mse', min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_depth=3, min_impurity_split=1e-07, init=None, random_state=None, max_features=None, verbose=0, max_leaf_nodes=None, warm_start=False, presort='auto'), #7

    discriminant_analysis.QuadraticDiscriminantAnalysis(priors=None, reg_param=0.0, store_covariances=False, tol=0.000001) #8
]

REGRESSORS = [
    neural_network.MLPRegressor(activation='relu', alpha=1e-05, batch_size='auto',
                                beta_1=0.9, beta_2=0.999, early_stopping=True,
                                epsilon=1e-08, hidden_layer_sizes=(100, 50), learning_rate='adaptive',
                                learning_rate_init=0.001, max_iter=50000, momentum=0.9,
                                nesterovs_momentum=True, power_t=0.5, random_state=None, shuffle=True,
                                solver='adam', tol=0.000001, validation_fraction=0.1, verbose=False,
                                warm_start=False), #1

    neural_network.MLPRegressor(activation='relu', alpha=1e-05, batch_size='auto',
                                beta_1=0.9, beta_2=0.999, early_stopping=True,
                                epsilon=1e-08, hidden_layer_sizes=(100, 50), learning_rate='adaptive',
                                learning_rate_init=0.001, max_iter=50000, momentum=0.9,
                                nesterovs_momentum=True, power_t=0.5, random_state=None, shuffle=True,
                                solver='sgd', tol=0.000001, validation_fraction=0.1, verbose=False,
                                warm_start=False), #2

    neighbors.KNeighborsRegressor(n_neighbors=5, weights='distance', algorithm='auto',
                                leaf_size=30, p=2, metric='minkowski',
                                metric_params=None, n_jobs=1), #3

    tree.DecisionTreeRegressor(criterion='mse', splitter='best', max_depth=None,
                                min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0,
                                max_features=None, random_state=None, max_leaf_nodes=None,
                                min_impurity_split=1e-07, presort=False), #4
    
    kernel_ridge.KernelRidge(alpha=1.0, coef0=1, degree=3, gamma=None, kernel='linear',
                                 kernel_params=None), #5

    ensemble.AdaBoostRegressor(base_estimator=None, n_estimators=1000, 
                        learning_rate=1.0, loss='exponential', random_state=None), #6

    ensemble.RandomForestRegressor(n_estimators=1000, criterion='mse', max_depth=None, 
                min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, 
                max_features='auto', max_leaf_nodes=None, min_impurity_split=1e-07, 
                bootstrap=True, oob_score=False, n_jobs=1, random_state=None, 
                verbose=0, warm_start=False), #7

    svm.SVR(kernel='rbf', degree=3, gamma='auto', coef0=0.0, tol=0.001, 
    C=1.0, epsilon=0.1, shrinking=True, cache_size=200, verbose=False, max_iter=-1), #8
]

def create_learn_model():
    scaler, input_data = get_eval_data()

    clf_array = []
    accuracy_array = []

    X_train, X_test, y_train, y_test = input_data[0]
    for clf in CLASSIFIERS:
        try:
            error=False
            clf.fit(X_train, y_train)
            accuracy = clf.score(X_test, y_test)
        except:
            error=True
        
        if error == False:
            print('Accuracy: ' + str(accuracy))
            clf_array.append(clf)
            accuracy_array.append(accuracy)
        else:
            print('Error encountered')
            clf_array.append(None)
            accuracy_array.append(0)

    index_clf, value_clf = max(enumerate(accuracy_array), key=itemgetter(1))
    print('Best classification model: ' + str(index_clf) + ' - Accuracy: ' + str(value_clf))

    # Save the classifier
    cl_file = random_file_name('models', 'cl_')
    pickle.dump(clf_array[index_clf], open(cl_file, 'wb'))

    new_clf = LearnModel()
    new_clf.accuracy = value_clf
    new_clf.data = cl_file
    new_clf.date = datetime.utcnow()
    new_clf.model_type = 0 # classifier
    new_clf.scaler = scaler
    new_clf.save()

    rg_array = []
    rg_accuracy_array = []
    
    X_train, X_test, y_train, y_test = input_data[1]
    for reg in REGRESSORS:
        try:
            error=False
            reg.fit(X_train, y_train)
            rg_accuracy = reg.score(X_test, y_test)
        except:
            error=True
        
        if error == False:
            print('Accuracy: ' + str(rg_accuracy))
            rg_array.append(reg)
            rg_accuracy_array.append(rg_accuracy)
        else:
            print('Error encountered')
            rg_array.append(None)
            rg_accuracy_array.append(0)
            
    index_rg, value_rg = max(enumerate(rg_accuracy_array), key=itemgetter(1))
    print('Best regression model: ' + str(index_rg) + ' - Accuracy: ' + str(value_rg))

    # Save the regressor
    rg_file = random_file_name('models', 'rg_')
    pickle.dump(rg_array[index_rg], open(rg_file, 'wb'))

    new_rg = LearnModel()
    new_rg.accuracy = value_rg
    new_rg.data = rg_file
    new_rg.date = datetime.utcnow()
    new_rg.model_type = 1 # regressor
    new_rg.scaler = scaler
    new_rg.save()

def get_learn_model(timestamp=0):
    if timestamp > 0:
        lookup_date = datetime.fromtimestamp(int(timestamp))
        clf_model = LearnModel.objects.filter(model_type=0, date__lte=lookup_date).earliest('date')
        rg_model = LearnModel.objects.filter(model_type=1, date__lte=lookup_date).earliest('date')
    else:
        clf_model = LearnModel.objects.filter(model_type=0).latest('date')
        rg_model = LearnModel.objects.filter(model_type=1).latest('date')

    clf = pickle.load(open(clf_model.data, 'rb'))
    reg = pickle.load(open(rg_model.data, 'rb'))
    clf_scaler = pickle.load(open(clf_model.scaler.data, 'rb'))
    reg_scaler = pickle.load(open(rg_model.scaler.data, 'rb'))

    return clf_scaler, clf, reg_scaler, reg

def predict_stock(code='', timestamp=0):
    queryset = DailyPrice.objects.all()

    if code != '':
        queryset = queryset.filter(stock__stock_code=code)

    if timestamp > 0:
        lookup_date = datetime.fromtimestamp(int(timestamp))
        queryset = queryset.filter(close_date__lte=lookup_date)
        price = queryset.earliest('close_date')
    else:
        price = queryset.latest('close_date')

    clf_scaler, clf, reg_scaler, reg = get_learn_model(timestamp)

    stock_code = price.stock.stock_code
    current_price = price.close_price
    input_data = numpy.array(get_input_array(price), dtype='f8')
    input_data = input_data.reshape(1, -1)

    clf_input = clf_scaler.transform(input_data)
    reg_input = reg_scaler.transform(input_data)

    predict_chance = clf.predict_proba(clf_input)
    predict_oscillate = reg.predict(reg_input)

    return stock_code, current_price, predict_chance, predict_oscillate, price_adjusted(predict_chance, predict_oscillate)

def predict_all(timestamp=0):
    if timestamp == None or int(timestamp) == 0:
        #try to get latest time
        max_date = DailyPrice.objects.all().aggregate(Max('close_date'))['close_date__max']
    else:
        max_date = datetime.fromtimestamp(int(timestamp))
    results = list(DailyPrice.objects.filter(close_date__date=max_date.date()))

    clf_scaler, clf, reg_scaler, reg = get_learn_model(timestamp)

    stock_code = [price.stock.stock_code for price in results]
    current_price = [price.close_price for price in results]
    input_data = numpy.array([get_input_array(price) for price in list(results)], dtype='f8')

    clf_input = clf_scaler.transform(input_data)
    reg_input = reg_scaler.transform(input_data)

    predict_chance = clf.predict_proba(clf_input)
    predict_oscillate = reg.predict(reg_input)

    return stock_code, current_price, predict_chance, predict_oscillate, price_adjusted(predict_chance, predict_oscillate)

def price_adjusted(predict_chance = [], predict_oscillate = []):
    results = []

    for i in range(len(predict_chance)):        
        negative_chance=predict_chance[i][0] 
        positive_chance=predict_chance[i][1]
        oscillate=predict_oscillate[i]

        if (positive_chance > negative_chance):
            if (oscillate > 0):
                results.append(oscillate * positive_chance)
            else:
                results.append(0)
        else:
            if (oscillate <= 0):
                results.append(oscillate * negative_chance)
            else:
                results.append(0)

    return results
