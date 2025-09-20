from typing import Any

from src.main.api.models.comparasion.model_comparasion_configuration import ModelComparasionConfigLoader
from src.main.api.models.comparasion.model_comparator import ModelComparator


class ModelAssertions:
    def __init__(self, request: Any, response: Any):
        self.request = request
        self.response = response

    def match(self) -> 'ModelAssertions':
        config_loader = ModelComparasionConfigLoader("model-comparison.properties")
        rule = config_loader.get_rule_for(self.request)
        if rule:
            result = ModelComparator.compare_fields(self.request, self.response, rule.field_mapping)
            if not result.is_success():
                raise AssertionError(f"Mismatched fields found: {result.message}")
        else:
            raise AssertionError(f"Rule not found for: {self.request.__class__.__name__}")
        return self
