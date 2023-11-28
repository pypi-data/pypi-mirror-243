import pytest
import pandas as pd
from pureml_evaluate.data_bias_metrics.class_imbalance import CI
from pureml_evaluate.data_bias_metrics.kullback_liebler_divergence import KL
from pureml_evaluate.data_bias_metrics.jensen_shannon_divergence import JS
import numpy as np

def test_CI():
    data = {
        'feature': [0.2, 0.4, 0.6, 0.8, 0.3, 0.7, 0.9, 0.5, 0.1, 0.6],
        'sensitive_facet_index': ['Female', 'Female', 'Male', 'Male', 'Female', 'Transgender', 'Male', 'Female', 'Transgender', 'Male']
    }
    df = pd.DataFrame(data)

    ci = CI()

    result = ci.compute(df['feature'], df['sensitive_facet_index'])

    print(result['column_imbalance'])
    assert result['column_imbalance']['Male'] == pytest.approx(0.2)
    assert result['column_imbalance']['Female'] == pytest.approx(0.2)
    assert result['column_imbalance']['Transgender'] == pytest.approx(0.6)

test_CI()

def test_KL():
    data = {
        'feature': [0.2, 0.4, 0.6, 0.8, 0.3, 0.7, 0.9, 0.5, 0.1, 0.6],
        'sensitive_facet': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'C']
    }
    df = pd.DataFrame(data)

    
    kl = KL()
    result = kl.compute(df['feature'], df['sensitive_facet'])

    print(result)
    assert result['kl']['A'] == pytest.approx(20.13820216112839)
    assert result['kl']['B'] == pytest.approx(69.81945839558972)
    assert result['kl']['C'] == pytest.approx(245.770895556853)


test_KL()



# def test_JS():
#     np.random.seed(42)
#     data = {
#         'feature': np.random.rand(10000),
#         'sensitive_facet': np.random.choice(['A', 'B', 'C', 'D'], size=10000)
#     }
#     df = pd.DataFrame(data)
#     js = JS()
    
#     result = js.compute(df['feature'], df['sensitive_facet'])

#     print(result)  # Helpful for debugging, remove in final test
#     assert result['js']['A'] == pytest.approx(0.5)
#     assert result['js']['B'] == pytest.approx(0.3)
#     assert result['js']['C'] == pytest.approx(0.2)

# test_JS()
