import joblib
import numpy.random as npr


def load_models(paths):
    models = []
    for path in paths:
        models.append(joblib.load(path))
    return models


def evaluate_prediction(y, y_pred):
    n_tp = 0
    n_tn = 0
    n_fp = 0
    n_fn = 0
    for iy, iy_pred in zip(y, y_pred):
        if iy == iy_pred:
            if iy == 1:
                n_tp += 1
            else:
                n_tn += 1
        else:
            if iy == 1:
                n_fn += 1
            else:
                n_fp += 1
    
    tpr = n_tp/(n_tp + n_fp) if (n_tp + n_fp) > 0 else 0
    fpr = n_fp/(n_fp + n_tn) if (n_fp + n_tn) > 0 else 0
    tnr = n_tn/(n_tn + n_fp) if (n_tn + n_fp) > 0 else 0
    fnr = n_fn/(n_fn + n_tn) if (n_fn + n_tn) > 0 else 0
    return {'tp': tpr, 'fp': fpr, 'tn': tnr, 'fn': fnr, 'n_tp': n_tp, 'n_tn': n_tn, 'n_fn': n_fn, 'n_fp': n_fp}
        
        
def random_classifier_prediction_evaluation(n_models, y_test, n_X, random_state=101):
    npr.seed(random_state)
    prediction_evaluation_list = []
    for _ in range(n_models):
        y_random = [npr.random() > 0.5 for _ in range(n_X)]
        evaluation = evaluate_prediction(y_test, y_random)
        prediction_evaluation_list.append(evaluation)
    return prediction_evaluation_list
