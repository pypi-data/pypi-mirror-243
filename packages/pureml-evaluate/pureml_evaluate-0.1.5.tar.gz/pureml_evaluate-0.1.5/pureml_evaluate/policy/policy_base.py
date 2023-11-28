from pydantic import BaseModel
from typing import List, Optional, Union
from pureml_evaluate.policy.metrics_import import metrics_to_class_name
from pureml_evaluate.metrics.fairness_for_policy import Fairness
import numpy as np
from collections import defaultdict
import pkg_resources


class PolicyBase(BaseModel):
    list_metrics: List[str] = []
    list_metrics_kwargs: List[dict] = None
    list_of_thresholds: dict = {}
    scores: dict = defaultdict(dict)  # Use defaultdict for nested dictionaries
    all_metrics_results = []

    def compute(self, references=None, predictions=None, prediction_scores=None, sensitive_features=None,
                productions=None, list_metrics=None, type=None, list_of_thresholds=None, **kwargs):

        # print(list_of_thresholds)
        try:
            list_metrics_objects = [
                metrics_to_class_name[metric_name] for metric_name in list_metrics]
        except Exception as e:
            print(e)

        if type == 'performance' and references is not None and predictions is not None:
            for m in list_metrics_objects:
                try:
                    result = m.compute(references, predictions,
                                       prediction_scores, **kwargs)
                    format_result = {'category': 'performance', 'risk': list(
                        result.keys())[0], 'value': list(result.values())[0]}
                    self.all_metrics_results.append(format_result)
                except Exception as e:
                    print(e)

        if type == 'drift' and references is not None and productions is not None:
            for m in list_metrics_objects:
                try:
                    result = m.compute(references, productions, **kwargs)
                    format_result = {'category': 'drift', 'risk': list(
                        result.keys())[0], 'value': list(result.values())[0]}
                    self.all_metrics_results.append(format_result)
                except Exception as e:
                    print(e)

        if type == 'fairness':
            fairness_evaluator = Fairness(references=references, predictions=predictions,
                                          sensitive_features=sensitive_features, prediction_scores=prediction_scores, **kwargs)
            fairness_evaluator.fairness_metrics = {
                k: v for k, v in fairness_evaluator.fairness_metrics.items() if k in list_metrics}
            fairness_evaluator.demography_metrics = {
                k: v for k, v in fairness_evaluator.demography_metrics.items() if k in list_metrics}
            result = fairness_evaluator.compute()
            all_metric_names = list(result.keys())
            format_result = {'fairness': {}}
            for metric_name in all_metric_names:
                format_result['fairness'][metric_name] = result[metric_name]['value']
                # format_result = {'category': 'fairness', 'risk' : metric_name, 'value' : result[metric_name]['value']}
            # print(f"Format Result: {format_result}")
            self.all_metrics_results.append(format_result)

        # print(f"Metrics Result: {self.all_metrics_results}")

        for result in self.all_metrics_results:
            if 'fairness' not in result.keys():
                category = result['category']
                metric = result['risk']
                self.scores[category][metric] = result['value']
            else:
                self.scores = self.all_metrics_results[0]

        # return self.scores
        risk_analysis = evaluate_metrics_against_thresholds(
            scores=self.scores, thresholds=list_of_thresholds)
        return risk_analysis


def evaluate_metrics_against_thresholds(scores, thresholds):
    evaluation_results = []

    for category, metrics in scores.items():
        for metric_name, metric_info in metrics.items():
            if isinstance(metric_info, dict) and 'value' in metric_info:
                value = metric_info['value']
            else:
                value = metric_info
            metric_name = metric_name.lower()
            threshold = thresholds.get(metric_name, None)
            severity = 'pass' if threshold is None or value <= threshold else 'fail'

            evaluation_result = {
                'category': category,
                'risk': metric_name,
                'value': value,
                'threshold': threshold,
                'severity': severity
            }

            evaluation_results.append(evaluation_result)

    return evaluation_results[0]
