from dazer import utils


def random_forests_feature_importances(models):
    feature_importances = []
    
    for model in models:
        importances = model.best_estimator_.feature_importances_.tolist()
        feature_importances.append(importances)

    return feature_importances

def random_forests_feature_importances_from_files(paths):
    models = utils.load_models(paths)
    feature_importances = random_forests_feature_importances(models)
    return feature_importances
