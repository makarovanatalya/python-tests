from abc import ABC
from typing import Any, List


class BaseSteps(ABC):
    def __init__(self, created_object: List[Any]):
        self.created_objects = created_object

    def add_created_object(self, created_object: Any):
        self.created_objects.append(created_object)