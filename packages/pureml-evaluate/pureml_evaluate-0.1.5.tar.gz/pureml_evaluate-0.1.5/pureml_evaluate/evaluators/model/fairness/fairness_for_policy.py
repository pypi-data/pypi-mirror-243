from fairlearn.metrics import MetricFrame
from fairlearn.metrics import (
    count,
    selection_rate,
    equalized_odds_difference,
    false_positive_rate,
    false_negative_rate,


    true_negative_rate,
    true_positive_rate,

    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference,
    equalized_odds_ratio,
)

from pydantic import BaseModel
import typing
import numpy as np
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.metrics import confusion_matrix


class Fairness(BaseModel):
    task_type = "fairness"
    evaluation_type = "fairness"

    references: typing.Any = None
    predictions: typing.Any = None
    sensitive_features: typing.Any = None
    prediction_scores: typing.Any = None
    label_type: str = "binary"

    metrics_to_report = [

        "balanced_accuracy",
        "balanced_acc_error",
        "selection_rate",
        "false_positive_rate",
        "false_positive_error",
        "false_negative_rate",
        "false_positive_error"

        "true_positive_rate",
        "true_negative_rate",

        "demographic_parity_difference",
        "demographic_parity_ratio",
        "equalized_odds_difference",
        "equalized_odds_ratio",
        "equalized_odds",
    ]
    kwargs: dict = None

    fairness_metrics: dict = {}
    demography_metrics: dict = {}
    

    def __init__(self,**data):
        super().__init__(**data)
        self.fairness_metrics = {
                # "count": count,
                "balanced_accuracy": balanced_accuracy_score,
                "balanced_acc_error": self.balanced_accuracy_error,
                "selection_rate": selection_rate,
                "false_positive_rate": false_positive_rate,
                "false_positive_error": self.false_positive_error,
                "false_negative_rate": false_negative_rate,
                "false_negative_error": self.false_negative_error,

                "true_positive_rate": true_positive_rate,
                "true_negative_rate": true_negative_rate,

            }


        self.demography_metrics = {

                "demographic_parity_difference": demographic_parity_difference,
                "demographic_parity_ratio": demographic_parity_ratio,
                "equalized_odds_difference": equalized_odds_difference,
                "equalized_odds_ratio": equalized_odds_ratio,
            }



    def setup_kwargs(self):
        try:
            if "average" not in self.kwargs:
                if self.label_type == "multilabel":
                    self.kwargs["average"] = "micro"
        except Exception as e:
            print(e)

    def compute_error_metric(self, metric_value, sample_size):
        """Compute standard error of a given metric based on the assumption of
        normal distribution.

        Parameters:
        metric_value: Value of the metric
        sample_size: Number of data points associated with the metric

        Returns:
        The standard error of the metric
        """
        metric_value = metric_value / sample_size
        return (
            1.96
            * np.sqrt(metric_value * (1.0 - metric_value))
            / np.sqrt(sample_size)
        )

    def false_positive_error(self, y_true, y_pred):
        """Compute the standard error for the false positive rate estimate."""
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return self.compute_error_metric(fp, tn + fp)

    def false_negative_error(self, y_true, y_pred):
        """Compute the standard error for the false negative rate estimate."""
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return self.compute_error_metric(fn, fn + tp)

    def balanced_accuracy_error(self, y_true, y_pred):
        """Compute the standard error for the balanced accuracy estimate."""
        fpr_error, fnr_error = self.false_positive_error(
            y_true, y_pred
        ), self.false_negative_error(y_true, y_pred)
        return np.sqrt(fnr_error**2 + fpr_error**2) / 2
    
    def equalized_odds(self,y_pred, y_true, sensitive_features):

        if sensitive_features is None:
            conf_mat = confusion_matrix(y_true, y_pred)
            fp = conf_mat[0,1] / (conf_mat[0,1] + conf_mat[0,0]) 
            fn = conf_mat[1,0] / (conf_mat[1,0] + conf_mat[1,1])
            return abs(fp - fn) < 0.05
        else:
            conf_matrices = {}
            for sens_group in np.unique(sensitive_features):
                mask = (sensitive_features == sens_group)
                y_pred_group = y_pred[mask]
                y_true_group = y_true[mask]
                conf_matrices[sens_group] = confusion_matrix(y_true_group, y_pred_group)
                
            # Calculate false positive and false negative rates for each group
            fp_rates = {}
            fn_rates = {}
            for group, conf_mat in conf_matrices.items():
                fp = conf_mat[0,1] / (conf_mat[0,1] + conf_mat[0,0])
                fn = conf_mat[1,0] / (conf_mat[1,0] + conf_mat[1,1])
                fp_rates[group] = fp 
                fn_rates[group] = fn

            fp_rates = list(fp_rates.values())  
            fn_rates = list(fn_rates.values())

            avg_fp_rate = np.mean(fp_rates)
            avg_fn_rate = np.mean(fn_rates)
            
            diff = np.abs(avg_fp_rate - avg_fn_rate)

            return diff  

    def setup(self):
        self.setup_kwargs()

    def compute(self):

        self.setup()

        metrics = {}

        for metric_name, metric_func in self.fairness_metrics.items():
            try:
                metrics[metric_name] = {'value':metric_func(
                    y_true=self.references, y_pred=self.predictions)}
            except Exception as e:
                print("Unable to compute", metric_name)
                print(e)

        for metric_name, metric_func in self.demography_metrics.items():
            try:                      
                metrics[metric_name] = {'value':metric_func(
                    y_true=self.references, y_pred=self.predictions,
                    sensitive_features=self.sensitive_features)}
            except Exception as e:
                print("Unable to compute", metric_name)
                print(e)

        return metrics