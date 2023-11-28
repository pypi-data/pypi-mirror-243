from .tabular_data import Tabular
from pydantic import BaseModel, root_validator
import typing
from typing import Literal
from enum import Enum


class TaskTypes(str, Enum):
    tabular = "tabular"


class Grader(BaseModel):
    # def __init__(self, task_type):
    task_type: TaskTypes

    
    scores: dict = {}
    task_grader: typing.Any = None

    # print(self.task_grader)

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def _set_fields(cls, values: dict) -> dict:

        task_type = values["task_type"]

        if task_type is not None:

            if task_type == TaskTypes.tabular:
                task_grader = Tabular()
            else:
                task_grader = None

            values["task_grader"] = task_grader

        return values

    def compute(self, data,  **kwargs):

        # print(self.task_grader)
        if self.task_grader is not None:
            # print('task grader is not none')
            self.task_grader.data = data
            # print("task grader", self.task_grader)
            print(f"Dataset: {self.task_grader.data}")

            self.scores = self.task_grader.compute()

        return self.scores


def grader(task_type, **kwargs):
    grade = Grader(task_type=task_type)

    return grade
