from .learndata import *
from sklearn import neural_network, neighbors, ensemble, svm, discriminant_analysis, kernel_ridge, tree
from datetime import datetime

from stocks.models import LearnModel

import pickle

CLASSIFIERS = [
    neural_network.MLPClassifier(hidden_layer_sizes=(100, 50), activation='logistic', solver='sgd', alpha=0.0001, batch_size='auto', learning_rate='adaptive', learning_rate_init=0.001, power_t=0.5, max_iter=50000, shuffle=True, random_state=None, tol=0.000001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08), #1

    neural_network.MLPClassifier(hidden_layer_sizes=(100, 50), activation='relu', solver='adam', alpha=0.0001, batch_size='auto', learning_rate='adaptive', learning_rate_init=0.001, power_t=0.5, max_iter=50000, shuffle=True, random_state=None, tol=0.000001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08), #2

    neighbors.KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=1), #3

    neighbors.KNeighborsClassifier(n_neighbors=5, weights='distance', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=1), #4

    ensemble.RandomForestClassifier(n_estimators=1000, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_split=1e-07, bootstrap=True, oob_score=False, n_jobs=-1, random_state=None, verbose=0, warm_start=False, class_weight=None), #5

    svm.SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None, random_state=None), #6

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
                                solver='sgd', tol=0.000001, validation_fraction=0.1, verbose=True,
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

def get_learn_model():
    X_train, X_test, y_train, y_test = get_eval_data()
    
    clf_array = []
    accuracy_array = []

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
            accuracy_array.append(abs(accuracy))
        else:
            print('Error encountered')
            clf_array.append(None)
            accuracy_array.append(0)

    index_clf, value_clf = max(enumerate(accuracy_array), key=itemgetter(1))
    print('Best classification model: ' + str(index_clf) + ' - Accuracy: ' + str(value_clf))

    # Save the classifier
    new_clf = LearnModel()
    new_clf.accuracy = value_clf
    new_clf.data = pickle.dumps(clf_array[index_clf])
    new_clf.date = datetime.utcnow()
    new_clf.model_type = 0 # classifier
    new_clf.save()

    rg_array = []
    rg_accuracy_array = []
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
            rg_accuracy_array.append(abs(rg_accuracy))
        else:
            print('Error encountered')
            rg_array.append(None)
            rg_accuracy_array.append(0)
            
    index_rg, value_rg = max(enumerate(rg_accuracy_array), key=itemgetter(1))
    print('Best regression model: ' + str(index_rg) + ' - Accuracy: ' + str(value_rg))

    # Save the regressor
    new_rg = LearnModel()
    new_rg.accuracy = value_rg
    new_rg.data = pickle.dumps(rg_array[index_rg])
    new_rg.date = datetime.utcnow()
    new_rg.model_type = 1 # regressor
    new_rg.save()
    