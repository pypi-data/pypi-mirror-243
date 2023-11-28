from pydantic import BaseModel
from .grade import Grader
from typing import Any, Union
from importlib import import_module
import numpy as np
from collections import defaultdict


class Evaluator(BaseModel):


    evaluators: Union[list[str], str]
    dataset: Any 
    grader: list[Grader] = []

    
    def load_graders(self):
        if type(self.evaluators) == str:
            self.grader.append(Grader(task_type=self.evaluators))
        elif type(self.evaluators) == list:
            for e in self.evaluators:
                self.grader.append(Grader(task_type=e))
        else:
            print("Unknown Evaluators: ", self.evaluators)

    def load(self):
        self.load_graders()

    def evaluate(self):

        values_all = defaultdict(dict)

        for g in self.grader:
            grader_type = g.task_grader

            values = g.compute(
                data = self.dataset
            )

            values_all[grader_type].update(values)
            #values_all[grader_type] = {'value' : values}
        
        values_all = dict(values_all)

        return values_all

def eval(dataset,evaluators):
    evaluator = Evaluator(
        dataset=dataset, evaluators=evaluators
    )

    evaluator.load()

    values_all = evaluator.evaluate()
    
    

    return values_all
