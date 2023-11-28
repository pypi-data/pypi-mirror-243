import pandas as pd
import numpy as np
from typing import Any, Dict
from pureml_evaluate.data_bias_metrics.data_bias_base import DataBiasBase

class JS(DataBiasBase):
    name: str  = 'js'
    input: str = 'dataframe'
    output: str = 'dataframe'
    kwargs: Dict = None

    def parse_data(self,data):
        return data
    
    def compute(self, feature: pd.Series, sensitive_facet_index: pd.Series) -> list:
        """
    Jensen-Shannon Divergence (JS) for multiple sensitive features.

    .. math::
        JS(Pa, Pd, P) = 0.5 [KL(Pa,P) + KL(Pd,P)] \\geq 0

    :param label: column of labels
    :param sensitive_facet: column indicating sensitive group (not necessarily boolean)
    :return: Jensen-Shannon (JS) divergence metric for each group vs the rest
    """
        unique_facets = sensitive_facet_index.unique()
        js_results = {}

        for facet in unique_facets:
            xs_a = feature[sensitive_facet_index != facet]
            xs_d = feature[sensitive_facet_index == facet]

            (Pa, Pd) = pdfs_aligned_nonzero(xs_a, xs_d)  # Assuming that this function is defined elsewhere
            P = 0.5 * (Pa + Pd)
            
            if len(Pa) == 0 or len(Pd) == 0 or len(P) == 0:
                raise ValueError("No instance of common facet found, dataset may be too small or improperly aligned")
            
            js = 0.5 * (np.sum(Pa * np.log(Pa / P)) + np.sum(Pd * np.log(Pd / P)))
            js_results[facet] = js
        
        return {
            self.name : js_results
        }
    
def pdfs_aligned_nonzero(xs_a: pd.Series, xs_d: pd.Series) -> (np.ndarray, np.ndarray):
    """
    Compute the aligned, non-zero PDFs of two series.

    :param xs_a: First series
    :param xs_d: Second series
    :return: Tuple of (Pa, Pd) where Pa and Pd are the aligned and non-zero probability distributions
    """
    # Count occurrences and convert to DataFrame for alignment
    counts_a = pd.DataFrame(xs_a.value_counts(normalize=True).reset_index())
    counts_d = pd.DataFrame(xs_d.value_counts(normalize=True).reset_index())
    
    # Renaming for clarity and merging
    counts_a.columns = ['value', 'prob_a']
    counts_d.columns = ['value', 'prob_d']
    merged = pd.merge(counts_a, counts_d, how='outer', on='value').fillna(0)
    
    # Ensuring that both PDFs are defined over the same space and have no zero-probability events in either
    nonzero = (merged['prob_a'] > 0) & (merged['prob_d'] > 0)
    aligned_nonzero = merged[nonzero]
    
    # Extracting and returning the final PDF arrays
    Pa = np.array(aligned_nonzero['prob_a'])
    Pd = np.array(aligned_nonzero['prob_d'])
    return (Pa, Pd)

    
