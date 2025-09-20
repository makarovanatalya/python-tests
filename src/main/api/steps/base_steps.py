from typing import Any, List


class BaseSteps:
    def __init__(self, created_object: List[Any]):
        self.created_obejcts = created_object