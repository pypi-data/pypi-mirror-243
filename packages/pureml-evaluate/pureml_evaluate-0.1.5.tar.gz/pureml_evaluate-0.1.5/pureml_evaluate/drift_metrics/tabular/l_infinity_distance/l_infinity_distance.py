from pureml_evaluate.drift_metrics.drift_base import DriftMetricBase
from typing import Any
import numpy as np

class LInfinityDistance(DriftMetricBase):
    name = 'l_infinity_distance'
    input_type: Any = 'dataframe'
    output_type: Any = dict
    kwargs: dict = None

    def parse_data(self, data):
        # Check if data is already a numpy array
      if isinstance(data, np.ndarray):
            return data.ravel()
        
        # If data is a pandas dataframe, converting it to numpy array
      try:
            return data.values.ravel()
      except AttributeError:
            raise TypeError("Expected input to be a numpy array or pandas DataFrame.")
      
    def compute(self, reference, production,columns, **kwargs):
        
        # Parse the data
        print(f"From L Infinity Distance: {reference.shape}")
        print(f"From L Infinity Distance: {type(reference)}")
        X = self.parse_data(reference)
        
        if production is None:
            mid = len(X) // 2
            Y = X[mid:]
            X = X[:mid]
        else:
            Y = self.parse_data(production)

        # Check if X and Y have the same length
        if len(X) != len(Y):
            raise ValueError("The lengths of the reference and production data do not match.")

        # Calculate L-infinity distance
        dist = np.max(np.abs(X - Y))

        return {
            self.name: {
                'value': dist
            }
        }