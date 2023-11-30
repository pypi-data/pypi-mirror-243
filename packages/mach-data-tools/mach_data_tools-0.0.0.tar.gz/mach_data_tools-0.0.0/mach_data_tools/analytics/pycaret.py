from pycaret.classification import setup, add_metric, remove_metric
from .metrics import ks_metric, auc_pr
from sklearn.metrics import average_precision_score


def setup_custom_metrics(*args, **kwargs) -> None:
    """
    Setup a Pycaret session with the custom metrics we use in the squad.
    """
    setup(*args, **kwargs)
    add_metric('KS', 'KS', ks_metric, 'pred_proba')
    add_metric('APS', 'APS', average_precision_score, 'pred_proba')
    add_metric('AUC_PR', 'PR AUC', auc_pr, 'pred_proba')
    remove_metric('Accuracy')
    remove_metric('Recall')
    remove_metric('Precision')
    remove_metric('F1')
    remove_metric('Kappa')
    remove_metric('MCC')
