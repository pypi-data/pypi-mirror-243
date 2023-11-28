from pydantic import BaseModel
from .grade import Grader
from typing import Any, Union
from importlib import import_module
import numpy as np
from collections import defaultdict
from .risk_evaluator_refactored import RiskEvaluator
from .graphs_generator import GraphsGenerator
import pkg_resources
from pureml_evaluate.utils.utils import get_data_dim, give_subsets
from pureml_evaluate.schema.metric import MetricTemplate, MetricResult, ColumnTemplate, MetricDictEnum


class Evaluator(BaseModel):
    y_true: Any
    y_pred: Any
    y_pred_scores: Any = None
    sensitive_features: Union[None, Any]

    evaluators: Union[list[str], str]
    grader: list[Grader] = []
    dataset: Any = None
    metrics: Any = None

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

    def load_graders(self):
        if type(self.evaluators) == str:
            self.grader.append(
                Grader(task_type=self.evaluators, metrics=self.metrics))
        elif type(self.evaluators) == list:
            for e in self.evaluators:
                self.grader.append(Grader(task_type=e, metrics=self.metrics))
        else:
            print("Unknown Evaluators: ", self.evaluators)

    def load(self):
        self.load_graders()

    def evaluate_one_set(self, y_true, y_pred, sensitive_features,
                         y_pred_scores, column: dict) -> MetricResult:
        metric_dict_list = []

        for g in self.grader:
            grader_type = g.task_grader.evaluation_type
            # print('grader_type: ', grader_type)
            metric_values = g.compute(
                references=y_true, predictions=y_pred,
                sensitive_features=sensitive_features, prediction_scores=y_pred_scores
            )
            # print('here')
            # print(metric_values)

            if grader_type != 'fairness':

                for value_key, values in metric_values.items():
                    metric_dict = MetricTemplate(
                        name=value_key,
                        category=grader_type,
                        value=values['value'],
                        status=None,
                        columns_sensitive=None
                    )
                    metric_dict_list.append(metric_dict)
            else:

                metric_dict_list += metric_values

        # print("metric_dict_list")
        # print(metric_dict_list)

        metric_result = MetricResult(
            column=column,
            metric=metric_dict_list
        )

        # print("metric_result")
        # print(metric_result)

        return metric_result.dict()

    def evaluate(self) -> MetricResult:

        column = [
            ColumnTemplate(name=MetricDictEnum.all.value,
                           value=MetricDictEnum.all.value)
        ]

        metric_result = self.evaluate_one_set(
            y_true=self.y_true,
            y_pred=self.y_pred,
            sensitive_features=self.sensitive_features,
            y_pred_scores=self.y_pred_scores,
            column=column
        )

        return metric_result

    def evaluate_subsets(self):

        if self.sensitive_features is None:  # If No Sensitive Features are given
            return None

        s_feat_dim, s_feat_df, column_names = get_data_dim(
            data=self.sensitive_features)

        subsets = give_subsets(
            s_feat_df=s_feat_df, column_names=column_names,
            y_true=self.y_true, y_pred=self.y_pred,
            y_pred_scores=self.y_pred_scores)

        print("Sensitive Columns: ", s_feat_dim,
              "Total subsets: ", len(subsets))

        metric_result_subsets = []

        for subset in subsets:

            column = subset['column']

            metric_result = self.evaluate_one_set(
                y_true=subset['y_true'],
                y_pred=subset['y_pred'],
                sensitive_features=subset['sensitive_features'],
                y_pred_scores=subset['y_pred_scores'],
                column=column
            )

            metric_result_subsets.append(metric_result)

        return metric_result_subsets


def eval(y_true, y_pred, sensitive_features, evaluators, y_pred_scores=None,
         metrics=None, threshold=80, path_to_config=None, as_html=False,
         as_pdf=False, pdf_file_name='metrics_graph.pdf'):
    evaluator = Evaluator(
        y_true=y_true, y_pred=y_pred,
        sensitive_features=sensitive_features, evaluators=evaluators,
        y_pred_scores=y_pred_scores,
        metrics=metrics
    )

    evaluator.load()

    values_all = evaluator.evaluate()
    values_subset_all = evaluator.evaluate_subsets()
    # values_subset_all = {}

    # if path_to_config is None:
    #     path_to_config = pkg_resources.resource_filename(
    #         __name__, 'config.json')
    # else:
    #     path_to_config = path_to_config
    # riskevaluate = RiskEvaluator(
    #     values_all, values_subset_all, path_to_config=path_to_config)
    # riskevaluate.compute_status()

    values = {
        "__all__": values_all,
        "__subsets__": values_subset_all
    }

    return values
