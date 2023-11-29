import pandas as pd
from feature_engine.selection import ProbeFeatureSelection
import shap
import sys
from sklearn.metrics import roc_auc_score, average_precision_score
from .metrics import auc_pr, ks_metric


def probe_feature_selection(selector: ProbeFeatureSelection, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    feature_decrease = True
    iterations = 1

    while feature_decrease:
        n_initial_features = len(X.columns)
        selector.fit(X, y)
        X = selector.transform(X)
        n_final_features = len(X.columns)
        feature_decrease = n_initial_features > n_final_features
        print(f'Iteration {iterations}: {n_initial_features} -> {n_final_features}')
        iterations += 1

    return X


def order_features_by_shap_values(df: pd.DataFrame, trained_model, ascending: bool = False) -> list[str]:
    explainer = shap.TreeExplainer(trained_model)
    shap_values = explainer.shap_values(df)
    df_shap = pd.DataFrame(shap_values, columns=df.columns)
    mean_shap = df_shap.abs().mean(0)
    mean_shap.sort_values(ascending=ascending, inplace=True)
    features_ordered = list(mean_shap.index)
    return features_ordered


def train_models_and_calculate_metrics(
            X_train: pd.DataFrame,
            y_train: pd.Series,
            X_test: pd.DataFrame,
            y_test: pd.Series,
            model,
            features_ordered: list[str]
        ) -> dict[str, list[float]]:
    metrics = {}
    for n_features in range(len(features_ordered)):
        sys.stdout.write(f"\rAnalizando: {n_features + 1}/{len(features_ordered)}")

        selected_variables = features_ordered[: n_features + 1]
        X_train_selected = X_train[selected_variables]
        X_test_selected = X_test[selected_variables]

        # fit model on all training data
        model.fit(X_train_selected, y_train)
        yhat = model.predict_proba(X_test_selected)

        # keep probabilities for the positive outcome only and calculate metrics
        yhat = yhat[:, 1]
        roc = roc_auc_score(y_test, yhat)
        aps = average_precision_score(y_test, yhat)
        pr = auc_pr(y_test, yhat)
        ks = ks_metric(y_test, yhat)

        if n_features == 0:
            metrics = {
                "roc": [],
                "aps": [],
                "pr": [],
                "ks": [],
            }

        metrics["roc"].append(roc)
        metrics["aps"].append(aps)
        metrics["pr"].append(pr)
        metrics["ks"].append(ks)

    return metrics
