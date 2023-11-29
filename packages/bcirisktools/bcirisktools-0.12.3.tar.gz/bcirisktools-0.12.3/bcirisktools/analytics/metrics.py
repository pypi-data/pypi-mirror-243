import numpy as np
from scipy.stats import ks_2samp
from sklearn.metrics import precision_recall_curve, auc


def ks_metric(y_true, y_score) -> float:
    y_true = np.array(y_true)
    y_score = np.array(y_score)

    x = y_score[y_true == 1]
    y = y_score[y_true == 0]
    ks_output = ks_2samp(x, y)

    return ks_output.statistic


def auc_pr(y_true, y_score) -> float:
    precision, recall, thresholds = precision_recall_curve(y_true, y_score)
    auc_precision_recall = auc(recall, precision)
    return auc_precision_recall
