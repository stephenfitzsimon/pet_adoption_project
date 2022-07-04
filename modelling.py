from itertools import product
#from statistics import multimode

import pandas as pd
from sklearn import metrics

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

import wrangle

RAND_SEED = 357

def make_decision_tree_model(X_train, y_train, X_validate, y_validate, depth, baseline_acc, return_model = False):
    """
    Makes a decision tree model and returns a dictionary containing calculated accuracy metrics
    """
    #make and fit the model
    clf = DecisionTreeClassifier(max_depth=depth, random_state=RAND_SEED)
    clf = clf.fit(X_train, y_train['target_outcome'])
    #make predictions
    y_pred = clf.predict(X_train)
    y_pred_val = clf.predict(X_validate)
    # calculate metrics
    metrics_dict = metrics.classification_report(y_train['target_outcome'], y_pred, output_dict=True, zero_division=True)
    metrics_dict_val = metrics.classification_report(y_validate['target_outcome'], y_pred_val, output_dict=True, zero_division=True)
    output = {
        'model':'Decision Tree Classifier',
        'attributes': f"max_depth={depth}",
        'train_accuracy': metrics_dict['accuracy'],
        'validate_accuracy': metrics_dict_val['accuracy'],
        'better_than_baseline':metrics_dict['accuracy'] > baseline_acc and metrics_dict_val['accuracy'] > baseline_acc
    }
    if return_model:
        return output, clf
    else:
        return output

def make_knn_model(X_train, y_train, X_validate, y_validate, k_neighbors, baseline_acc, return_model = False):
    """
    Makes a K-nearest neighbors model and returns a dictionary containing calculated accuracy metrics
    """
    #make and fit the model
    knn = KNeighborsClassifier(n_neighbors=k_neighbors)
    knn = knn.fit(X_train, y_train['target_outcome'])
    #make prediction
    y_pred = knn.predict(X_train)
    y_pred_val = knn.predict(X_validate)
    #calculate metrics
    metrics_dict = metrics.classification_report(y_train['target_outcome'], y_pred, output_dict=True, zero_division=True)
    metrics_dict_val = metrics.classification_report(y_validate['target_outcome'], y_pred_val, output_dict=True, zero_division=True)
    output = {
        'model':'K-Nearest Neighbors',
        'attributes':f"k-neighbors = {k_neighbors}",
        'train_accuracy': metrics_dict['accuracy'],
        'validate_accuracy': metrics_dict_val['accuracy'],
        'better_than_baseline': metrics_dict['accuracy'] > baseline_acc and metrics_dict_val['accuracy'] > baseline_acc
    }
    if return_model:
        return output, knn
    else:
        return output

def make_random_forest_model(X_train, y_train, X_validate, y_validate, leaf, depth, trees, baseline_acc, return_model = False):
    """
    Makes a random forest model and returns a dictionary containing calculated accuracy metrics
    """
    #make and fit the model
    rf = RandomForestClassifier(min_samples_leaf = leaf, max_depth=depth, n_estimators=trees, random_state=RAND_SEED)
    rf = rf.fit(X_train, y_train['target_outcome'])
    #make predictions
    y_pred = rf.predict(X_train)
    y_pred_val = rf.predict(X_validate)
    #calculate the metrics
    metrics_dict = metrics.classification_report(y_train['target_outcome'], y_pred, output_dict=True, zero_division=True)
    metrics_dict_val = metrics.classification_report(y_validate['target_outcome'], y_pred_val, output_dict=True, zero_division=True)
    output = {
        'model':'Random Forest Model',
        'attributes':f"leafs = {leaf} : depth = {depth} : trees = {trees}",
        'train_accuracy': metrics_dict['accuracy'],
        'validate_accuracy': metrics_dict_val['accuracy'],
        'better_than_baseline': metrics_dict['accuracy'] > baseline_acc and metrics_dict_val['accuracy'] > baseline_acc
    }
    if return_model:
        return output, rf
    else:
        return output

def make_logistic_regression_model(X_train, y_train, X_validate, y_validate, solv_algo, baseline_acc, return_model = False):
    """
    Makes a logistic regression model and returns a dictionary containing calculated accuracy metrics
    """
    #make and fit the model
    lr = LogisticRegression(multi_class='multinomial',solver=solv_algo, random_state=RAND_SEED,max_iter=5_000).fit(X_train, y_train['target_outcome'])
    #make prediction
    y_pred = lr.predict(X_train)
    y_pred_val = lr.predict(X_validate)
    #calculate metrics
    metrics_dict = metrics.classification_report(y_train['target_outcome'], y_pred, output_dict=True, zero_division=True)
    metrics_dict_val = metrics.classification_report(y_validate['target_outcome'], y_pred_val, output_dict=True, zero_division=True)
    output = {
        'model':'Logistic Regression Model',
        'attributes':f"solver = {solv_algo}",
        'train_accuracy': metrics_dict['accuracy'],
        'validate_accuracy': metrics_dict_val['accuracy'],
        'better_than_baseline': metrics_dict['accuracy'] > baseline_acc and metrics_dict_val['accuracy'] > baseline_acc
    }
    if return_model:
        return output, lr
    else:
        return output

def make_extra_trees_model(X_train, y_train, X_validate, y_validate, leaf, depth, trees, baseline_acc, return_model = False):
    """
    Makes an extra trees model and returns a dictionary containing calculated accuracy metrics
    """
    #make and fit the model
    et = ExtraTreesClassifier(min_samples_leaf = leaf, max_depth=depth, n_estimators=trees, random_state=RAND_SEED)
    et = et.fit(X_train, y_train['target_outcome'])
    #make predictions
    y_pred = et.predict(X_train)
    y_pred_val = et.predict(X_validate)
    #calculate the metrics
    metrics_dict = metrics.classification_report(y_train['target_outcome'], y_pred, output_dict=True, zero_division=True)
    metrics_dict_val = metrics.classification_report(y_validate['target_outcome'], y_pred_val, output_dict=True, zero_division=True)
    output = {
        'model':'Extra Trees Model',
        'attributes':f"leafs = {leaf} : depth = {depth} : trees = {trees}",
        'train_accuracy': metrics_dict['accuracy'],
        'validate_accuracy': metrics_dict_val['accuracy'],
        'better_than_baseline': metrics_dict['accuracy'] > baseline_acc and metrics_dict_val['accuracy'] > baseline_acc
    }
    if return_model:
        return output, et
    else:
        return output

def make_mass_models(X_train, y_train, X_validate, y_validate, baseline_accuracy):
    """
    Passes a series of parameters to the model functions to produce a dataframe
    containing model metrics to compare
    """
    outputs = []
    #make decision tree and knn models
    for i in range(2, 25):
        output_tree = make_decision_tree_model(X_train, y_train, X_validate, y_validate, depth=i, baseline_acc=baseline_accuracy)
        print(f"\rFinished Decision Tree with depth {i}", end = '')
        output_knn = make_knn_model(X_train, y_train, X_validate, y_validate, k_neighbors=i, baseline_acc=baseline_accuracy)
        print(f"\rFinished KNN with k {i}", end = '')
        outputs.append(output_tree)
        outputs.append(output_knn)
    # make parameter set for the random forest and extra tree models
    rand_forest_params = return_product(5, 5, 5)
    #make the random forest and extra trees models
    for prod in rand_forest_params:
        output_rf = make_random_forest_model(X_train, y_train, X_validate, y_validate, leaf=prod[0], depth=prod[1], trees = prod[2], baseline_acc=baseline_accuracy)
        print(f"\rFinished RandomForest with leaf {prod[0]}, depth {prod[1]}, and trees {prod[2]}", end = '')
        output_et = make_extra_trees_model(X_train, y_train, X_validate, y_validate, leaf=prod[0], depth=prod[1], trees = prod[2], baseline_acc=baseline_accuracy)
        print(f"\rFinished ExtraTrees with leaf {prod[0]}, depth {prod[1]}, and trees {prod[2]}", end = '')
        outputs.append(output_rf)
        outputs.append(output_et)
    #solvers for the logistic regression
    linear_solvers = ['newton-cg', 'lbfgs', 'sag', 'saga']
    #make logistic regression models
    for solv in linear_solvers:
        output_rf = make_logistic_regression_model(X_train, y_train, X_validate, y_validate, solv_algo=solv, baseline_acc=baseline_accuracy)
        print(f"\rFinished Logistic Regression with solver {solv}", end = '')
        outputs.append(output_rf)
    return pd.DataFrame(outputs)

def return_product(l, d, t):
    """
    makes a itertools object iterable for the random forest and extra trees models
    """
    #make the range sets
    leaf_vals = range(1,l)
    depth_vals = range(2,d)
    #make tree values starting at 100 and going up in steps of 50
    tree_values = range(100, t*100, 50)
    #make the cartesian product
    product_output = product(leaf_vals, depth_vals, tree_values)
    return product_output
    
def models_mass(train, validate, baseline_accuracy):
    """
    Flow control function to make the mass models
    """
    X_train, y_train = wrangle.make_model_sets(train)
    X_validate, y_validate = wrangle.make_model_sets(validate)
    return make_mass_models(X_train, y_train, X_validate, y_validate, baseline_accuracy)

def make_voting_ensemble(X_train, y_train, X_validate, y_validate, models, baseline_acc, return_model = False):
    """
    Makes an ensemble voting model and returns metrics on it
    """
    #get the esitmators from the passed models
    voting_models = []
    for key in models:
        voting_models.append((key, models[key]))
    #make the model
    ens = VotingClassifier(estimators=voting_models).fit(X_train, y_train['target_outcome'])
    #predict on the model
    y_pred = ens.predict(X_train)
    y_pred_val = ens.predict(X_validate)
    #calculate the metrics
    metrics_dict = metrics.classification_report(y_train['target_outcome'], y_pred, output_dict=True, zero_division=True)
    metrics_dict_val = metrics.classification_report(y_validate['target_outcome'], y_pred_val, output_dict=True, zero_division=True)
    output = {
        'model':'Voting Classifier Modell',
        'attributes':f"Includes all models",
        'train_accuracy': metrics_dict['accuracy'],
        'validate_accuracy': metrics_dict_val['accuracy'],
        'better_than_baseline': metrics_dict['accuracy'] > baseline_acc and metrics_dict_val['accuracy'] > baseline_acc
    }
    if return_model:
        return output, ens
    else:
        return output


def make_final_report_models(train, validate, baseline_accuracy):
    """
    Flow control function to make models selected for the final report
    """
    #split the data into target variable
    X_train, y_train = wrangle.make_model_sets(train)
    X_validate, y_validate = wrangle.make_model_sets(validate)
    models = dict()
    outputs = []
    #make the models and add to the output variables
    dt_11_output, dt_11_model = make_decision_tree_model(X_train, y_train, X_validate, y_validate, depth=11, baseline_acc=baseline_accuracy, return_model=True)
    outputs.append(dt_11_output)
    models['dt_11'] = dt_11_model
    print(f"\rFinished Decision Tree 11\t\t\t\t\t", end = '')
    dt_6_output, dt_6_model = make_decision_tree_model(X_train, y_train, X_validate, y_validate, depth=6, baseline_acc=baseline_accuracy, return_model=True)
    outputs.append(dt_6_output)
    models['dt_6'] = dt_6_model
    print(f"\rFinished Decision Tree 6\t\t\t\t\t", end = '')
    knn_output, knn_model = make_knn_model(X_train, y_train, X_validate, y_validate, k_neighbors=20, baseline_acc=baseline_accuracy, return_model=True)
    outputs.append(knn_output)
    models['knn'] = knn_model
    print(f"\rFinished KNN\t\t\t\t\t\t\t\t", end = '')
    logR_output, logR_model = make_logistic_regression_model(X_train, y_train, X_validate, y_validate, solv_algo='newton-cg', baseline_acc=baseline_accuracy, return_model=True)
    outputs.append(logR_output)
    models['lr'] = logR_model
    print(f"\rFinished Logistic Regression\t\t\t\t\t", end = '')
    rf_100_output, rf_100_model = make_random_forest_model(X_train, y_train, X_validate, y_validate, leaf=4, depth=4, trees=100, baseline_acc=baseline_accuracy, return_model=True)
    outputs.append(rf_100_output)
    models['rf_100'] = rf_100_model
    print(f"\rFinished Random Forest 100\t\t\t\t\t", end = '')
    rf_250_output, rf_250_model = make_random_forest_model(X_train, y_train, X_validate, y_validate, leaf=4, depth=4, trees=250, baseline_acc=baseline_accuracy, return_model=True)
    outputs.append(rf_250_output)
    models['rf_250'] = rf_250_model
    print(f"\rFinished Random Forest 250\t\t\t\t\t", end = '')
    et_output, et_model = make_extra_trees_model(X_train, y_train, X_validate, y_validate, leaf=4, depth=4, trees=150, baseline_acc=baseline_accuracy, return_model=True)
    outputs.append(et_output)
    models['et'] = et_model
    print(f"\rFinished Extra Trees\t\t\t\t\t", end = '')
    ens_output, ens_model = make_voting_ensemble(X_train, y_train, X_validate, y_validate, models, baseline_acc=baseline_accuracy, return_model = True)
    outputs.append(ens_output)
    models['ens'] = ens_model
    print(f"\rFinished Voting Ensemble\t\t\t\t", end = '')
    output_df = pd.DataFrame(outputs)
    output_df['difference'] = output_df['train_accuracy'] - output_df['validate_accuracy']
    return output_df, models

def test_model(df, model, model_name, accuracy_information, baseline_accuracy):
    """"
    Runs a model on test data and returns the metrics for the model across all the data sets
    """
    # split the data
    X, y = wrangle.make_model_sets(df)
    #predict
    y_pred = model.predict(X)
    #calculate the metrics
    metrics_dict = metrics.classification_report(y['target_outcome'], y_pred, output_dict=True, zero_division=True)
    output = []
    output_metrics = {
        'model' : model_name, 
        'train_accuracy' : accuracy_information['train_accuracy'],
        'validate_accuracy' : accuracy_information['validate_accuracy'],
        'test_accuracy' : metrics_dict['accuracy'],
        'better_than_baseline' : metrics_dict['accuracy'] > baseline_accuracy
    }
    output.append(output_metrics)
    return pd.DataFrame(output)