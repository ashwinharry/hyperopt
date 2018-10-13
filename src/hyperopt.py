from sklearn.externals.joblib import Parallel, delayed
import itertools
import sklearn.model_selection
import sklearn.linear_model
import sklearn.tree
import numpy as np
import sys
import json
import datetime

def gridsearch(estimator, parameters, train_x, train_y):
    time=datetime.datetime.now()
    clf = sklearn.model_selection.GridSearchCV(estimator, parameters, n_jobs=-1)
    clf.fit(train_x, train_y)
    elapsed = (datetime.datetime.now() - time).seconds
    # return clf.cv_results_
    return clf.best_params_, clf.best_score_, elapsed

# return times also
def randomsearch(estimator, parameters, train_x, train_y):
    time=datetime.datetime.now()
    clf = sklearn.model_selection.RandomizedSearchCV(estimator, parameters, n_jobs=-1)
    clf.fit(train_x, train_y)
    elapsed = (datetime.datetime.now() - time).seconds
    # return clf.cv_results_
    return clf.best_params_, clf.best_score_, elapsed

# def plotsamplesaccuracy():
#     pass

def decisiontreeclassifier():
    parameters = {
        'max_depth': [1,3,5,6,7,8,10,11],
        'criterion': ['gini', 'entropy'],

    }
    estimator = sklearn.tree.DecisionTreeClassifier()
    return estimator, parameters

def logisticregression():
    parameters = {'penalty': ['l1', 'l2'], 'C': [1e-2, 1e-1, 1, 10, 100]}
    estimator = sklearn.linear_model.LogisticRegression()
    return estimator, parameters

class Model:
    def __init__(self, *args, **kwargs):
        # if 'modelclass' in kwargs:
        #     self.modelclass = kwargs['modelclass']
        # else:
        #     self.modelclass = sklearn.linear_model.LogisticRegression

        # self.model = self.modelclass()
        self.modelestimators = {
            'logisticregression': sklearn.linear_model.LogisticRegression(),
            'decisiontreeclassifier': sklearn.tree.DecisionTreeClassifier(),
        }
    def getdefaultparameters(self):
        with open('src/defaulthyperparameters.json') as f:
            self.defaultparamers = json.load(f)
        return self.defaultparamers

    # def fit(self, train_x, train_y):
    #     self.model.fit(train_x, train_y)
    
    def run(self, train_x, train_y, modelclass, parameters):
        estimator = self.modelestimators[modelclass]
        if parameters is None:
            parameters = self.getdefaultparameters()
        
        parameters = parameters[modelclass]
        parameters = numerify(parameters)

        best_params_grid, best_score_grid, elapsed_grid = gridsearch(estimator, parameters, train_x, train_y)
        best_params_random, best_score_random, elapsed_random = randomsearch(estimator, parameters, train_x, train_y)
        return best_params_grid, best_score_grid, elapsed_grid, best_params_random, best_score_random, elapsed_random
        # return bestparams_random

def jsonify(best_params_grid, best_score_grid, elapsed_grid, best_params_random, best_score_random, elapsed_random):
    jsonified = {
        "grid":{
            "parameters": best_params_grid,
            "score": best_score_grid,
            "elapsed": elapsed_grid
        },
        "random":{
            "parameters": best_params_random,
            "score": best_score_random,
            "elapsed": elapsed_random
        }
    }
    return jsonified

def numerify(parameters):
    for key in parameters:
        try:
            parameters[key] = [float(val) for val in parameters[key]]
        except ValueError:
            pass
    return parameters


def main():
    data = np.stack([np.append(30*(i%2+1)+15*np.random.randn(2),(i%2+1)) for i in range(1,100000)])
    train_x = data[:,0:2]
    train_y = data[:,2]
    model = Model()

    modelclass = sys.argv[1]
    hyperparametersfile = sys.argv[2]
    with open(hyperparametersfile) as f:
        hyperparameters = json.load(f)

    try:
        best_params_grid, best_score_grid, elapsed_grid, best_params_random, best_score_random, elapsed_random = model.run(train_x, train_y, modelclass, hyperparameters)
        print(json.dumps(jsonify(best_params_grid, best_score_grid, elapsed_grid, best_params_random, best_score_random, elapsed_random)))
    except:
        print('Oh nooooo')
    
    sys.stdout.flush()


main()