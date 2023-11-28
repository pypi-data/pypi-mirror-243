import pandas as pd
from pureml_evaluate.data_bias_metrics.data_bias_base import DataBiasBase
from typing import Any, Dict

class CI(DataBiasBase):
    name: str = 'column_imbalance'
    input: str = 'dataframe'
    output: str = 'dataframe'
    kwargs: Dict = None


    def parse_data(self,data):
        return data
    
    def compute(self, feature: pd.Series, sensitive_facet_index: pd.Series) -> list:
        r"""
        Class Imbalance (CI)

        :param feature: input feature
        :param sensitive_facet_index: column indicating sensitive group
        :return: a list of floats, each indicating the under-representation or over-representation
            of a sensitive class.

        .. math::
            CI = \frac{na-nd}{na+nd}

        Bias is often generated from an under-representation of
        the sensitive class in the dataset, especially if the desired “golden truth”
        is equality across classes. Imbalance carries over into model predictions.
        We will report all measures in differences and normalized differences. Since
        the measures are often probabilities or proportions, the differences will lie in

        We define CI = (np − p)/(np + p). Where np is the number of instances in the not sensitive group
        and p is the number of instances in the sensitive group.
        """

        unique_groups = sensitive_facet_index.unique()
        ci_values = []

        for group in unique_groups:
            pos = len(feature[sensitive_facet_index == group])
            neg = len(feature[sensitive_facet_index != group])
            q = pos + neg

            if neg == 0:
                raise ValueError(f"CI: negated facet set for group '{group}' is empty. Check that x[~facet] has non-zero length.")
            if pos == 0:
                raise ValueError(f"CI: facet set for group '{group}' is empty. Check that x[facet] has non-zero length.")

            assert q != 0
            ci = float(neg - pos) / q
            ci_values.append(ci)

        result = {}
        for i in range(len(unique_groups)):
            result[unique_groups[i]] = ci_values[i]

        return {
            self.name : result
        }
