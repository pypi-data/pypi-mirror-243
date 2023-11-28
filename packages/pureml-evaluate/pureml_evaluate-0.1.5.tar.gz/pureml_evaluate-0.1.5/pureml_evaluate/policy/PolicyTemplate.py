from typing import Any, Dict
from pydantic import BaseModel



class PolicyTemplate(BaseModel):
    name: str = 'NYC144'


    def operational_metrics():
        list_of_metrics  = ['Accuracy','F1','Recall']
        list_of_thresholds = {'accuracy':0.8,'f1' : 0.7,'recall' : 0.6}

        return list_of_metrics, list_of_thresholds

    def fairness_metrics():
        list_of_metrics  = ["balanced_acc_error",
        "selection_rate",
        "false_positive_rate",
        "false_positive_error"]
        list_of_thresholds = {'balanced_acc_error':0.8,'selection_rate' : 0.7,'false_positive_rate' : 0.6,'false_positive_error':0.5}

        return list_of_metrics, list_of_thresholds
    
    def drift_metrics():
        pass 
    