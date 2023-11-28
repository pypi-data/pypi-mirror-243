from typing import Any, Dict, List, Optional, Tuple, Union
import pandas as pd
from pydantic import BaseModel
from abc import ABC,abstractmethod, abstractproperty



class DataBiasBase(BaseModel):
    name: str = 'class_imbalance'
    input_type: Any = 'dataframe'
    output_type: Any = 'dataframe'
    kwargs: Dict = None

    @abstractmethod
    def parse_data(self):
        pass


    @abstractmethod
    def compute(self):
        pass