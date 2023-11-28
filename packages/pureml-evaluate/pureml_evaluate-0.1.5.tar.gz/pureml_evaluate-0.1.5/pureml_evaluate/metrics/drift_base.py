from typing import List, Dict, Any, Union, Optional
import pandas as pd
from pydantic import BaseModel
from abc import ABC, abstractmethod, abstractproperty


class DriftMetricBase(ABC, BaseModel):
    name : str = 'drift_metric'
    input_type : str = 'dataframe'
    output_type : str = 'dataframe'

    @abstractmethod
    def parse_data(self):
        pass

    @abstractmethod
    def compute(self):
        pass