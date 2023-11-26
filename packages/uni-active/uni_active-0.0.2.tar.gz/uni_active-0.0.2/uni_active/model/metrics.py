import numpy as np
from sklearn import metrics


def mae2d(y, y_pre):
    return np.average(y - y_pre, axis=0)


def mape(y_true, y_predict):
    return np.sum(np.abs(y_true - y_predict)) / np.max(np.abs(y_true - y_predict))


def rmse(y_true, y_predict):
    return (np.sum((y_true - y_predict) ** 2)) ** 0.5


def nrmse(y_true, y_predict):
    return (np.sum((y_true - y_predict) ** 2)) ** 0.5 / np.max(np.abs(y_true - y_predict))


def nmae(y_true, y_predict):
    return np.sum(np.abs(y_true - y_predict)) / np.max(np.abs(y_true - y_predict))


def me(y_true, y_predict):
    return np.max(np.abs(y_true - y_predict))


server_scoring = {"mae2d": mae2d,
                  "rmse": rmse,
                  "mape": mape,
                  "nrmse": nrmse,
                  "nmae": nmae,
                  "me": me
                  }

sklearn_scoring = [
    "accuracy_score",
    "adjusted_mutual_info_score",
    "adjusted_rand_score",
    "auc",
    "average_precision_score",
    "balanced_accuracy_score",
    "calinski_harabasz_score",
    "check_scoring",
    "class_likelihood_ratios",
    "classification_report",
    "cluster",
    "cohen_kappa_score",
    "completeness_score",
    "ConfusionMatrixDisplay",
    "confusion_matrix",
    "consensus_score",
    "coverage_error",
    "d2_tweedie_score",
    "d2_absolute_error_score",
    "d2_pinball_score",
    "dcg_score",
    "davies_bouldin_score",
    "DetCurveDisplay",
    "det_curve",
    "DistanceMetric",
    "euclidean_distances",
    "explained_variance_score",
    "f1_score",
    "fbeta_score",
    "fowlkes_mallows_score",
    "get_scorer",
    "hamming_loss",
    "hinge_loss",
    "homogeneity_completeness_v_measure",
    "homogeneity_score",
    "jaccard_score",
    "label_ranking_average_precision_score",
    "label_ranking_loss",
    "log_loss",
    "make_scorer",
    "nan_euclidean_distances",
    "matthews_corrcoef",
    "max_error",
    "mean_absolute_error",
    "mean_squared_error",
    "mean_squared_log_error",
    "mean_pinball_loss",
    "mean_poisson_deviance",
    "mean_gamma_deviance",
    "mean_tweedie_deviance",
    "median_absolute_error",
    "mean_absolute_percentage_error",
    "multilabel_confusion_matrix",
    "mutual_info_score",
    "ndcg_score",
    "normalized_mutual_info_score",
    "pair_confusion_matrix",
    "pairwise_distances",
    "pairwise_distances_argmin",
    "pairwise_distances_argmin_min",
    "pairwise_distances_chunked",
    "pairwise_kernels",
    "PrecisionRecallDisplay",
    "precision_recall_curve",
    "precision_recall_fscore_support",
    "precision_score",
    "PredictionErrorDisplay",
    "r2_score",
    "rand_score",
    "recall_score",
    "RocCurveDisplay",
    "roc_auc_score",
    "roc_curve",
    "get_scorer_names",
    "silhouette_samples",
    "silhouette_score",
    "top_k_accuracy_score",
    "v_measure_score",
    "zero_one_loss",
    "brier_score_loss",
]


def get_score(scoring: str, **kwargs):
    """
    The function `get_score` takes in the true labels `y`, predicted labels `y_pre`, a scoring metric as
    a string, and additional keyword arguments, and returns the corresponding scoring metric.
    
    Args:
      scoring (str): The scoring parameter is a string that specifies the scoring metric to be used for
    evaluating the performance of a machine learning model. It can be any valid scoring metric supported
    by scikit-learn or a custom scoring metric defined by the server_scoring dictionary.
    
    Returns:
      the scoring object based on the input scoring string. If the scoring string is a valid scoring
    metric from the sklearn library, it will return the corresponding scoring object from the sklearn
    library. If the scoring string is not a valid scoring metric from the sklearn library, it will
    return the corresponding scoring object from the server_scoring dictionary.
    """

    if scoring in sklearn_scoring:
        scoring = getattr(metrics, scoring)
    else:
        scoring = server_scoring[str]

    return scoring
