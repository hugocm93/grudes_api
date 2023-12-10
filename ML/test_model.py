import pandas as pd
import numpy as np
import joblib as jl
from sklearn.model_selection import train_test_split
import sklearn.metrics as skm 
import warnings

def load_dataset():
    return pd.read_json("./ML/dataset/train.json")

def load_test_data():
    recipes = load_dataset() 

    test_size = 0.20
    seed = 7
    np.random.seed(7)

    X = recipes.values[:,2]
    X = [' '.join(ingredients) for ingredients in X]

    Y = recipes.values[:,1]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
        test_size=test_size, shuffle=True, random_state=seed, stratify=Y)

    return X_test, Y_test

def assess(classifier, X_test, Y_test):

    prediction = classifier.predict(X_test)
            
    return (skm.accuracy_score(Y_test, prediction),
            skm.recall_score(Y_test, prediction, average='macro'),
            skm.precision_score(Y_test, prediction, average='macro'),
            skm.f1_score(Y_test, prediction, average='macro'))

def test_key_ingredients():

    classifier = jl.load('./ML/model.joblib');

    assert classifier.predict(['olive oil pasta tomato'])[0]  == 'italian'
    assert classifier.predict(['rice beans'])[0]              == 'mexican'
    assert classifier.predict(['soy souce rice'])[0]          == 'japanese'
    assert classifier.predict(['egg flour sugar'])[0]         == 'french'
    assert classifier.predict(['cabbage pepper sausage'])[0]  == 'irish'
    assert classifier.predict(['brocollis tofu rice'])[0]     == 'chinese'

def test_metrics():

    warnings.filterwarnings("ignore", category=DeprecationWarning) 

    classifier = jl.load('./ML/model_dev.joblib');
    X_test, Y_test = load_test_data();

    accuracy, recall_score, precision_score, f1_score = assess(classifier, X_test, Y_test)

    print(accuracy)
    print(recall_score)
    print(precision_score)
    print(f1_score)

    assert accuracy > 0.80
    assert recall_score > 0.70
    assert precision_score > 0.70
    assert f1_score > 0.70
