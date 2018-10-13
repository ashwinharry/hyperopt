from sklearn.externals.joblib import Parallel, delayed
import itertools
import sklearn.model_selection
import sklearn.linear_model
import sklearn.tree
import numpy as np
import sys
import json

def gridsearch(estimator, parameters, train_x, train_y):
    clf = sklearn.model_selection.GridSearchCV(estimator, parameters, n_jobs=-1)
    clf.fit(train_x, train_y)
    return clf.best_params_, clf.best_score_

# return times also
def randomsearch(estimator, parameters, train_x, train_y):
    clf = sklearn.model_selection.RandomizedSearchCV(estimator, parameters, n_jobs=-1)
    clf.fit(train_x, train_y)
    return clf.best_params_, clf.best_score_

def plotsamplesaccuracy():
    pass

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
        # estimator, parameters = decisiontreeclassifier()
        bestparams_grid = gridsearch(estimator, parameters, train_x, train_y)
        bestparams_random = randomsearch(estimator, parameters, train_x, train_y)
        return bestparams_grid, bestparams_random
        # return bestparams_random

def main():
    data = np.stack([np.append(30*(i%2+1)+15*np.random.randn(2),(i%2+1)) for i in range(1,200000)])
    train_x = data[:,0:2]
    train_y = data[:,2]
    model = Model()

    print(sys.argv)
    modelclass = sys.argv[1]
    hyperparametersfile = sys.argv[2]
    with open(hyperparametersfile) as f:
        hyperparameters = json.load(f)

    print(model.run(train_x, train_y, modelclass, hyperparameters))

main()