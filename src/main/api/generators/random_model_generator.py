from datetime import datetime, timedelta
import random
import uuid
from typing import Any, get_type_hints, get_origin, Annotated, get_args
import rstr
from src.main.api.generators.generating_rule import GeneratingRule


class RandomModelGenerator:
    @staticmethod
    def generate(cls: type) -> Any:
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}

        for filed_name, annotated_type in type_hints.items():
            rule = None

            if get_origin(annotated_type) is Annotated:
                actual_type, *annotation = get_args(annotated_type)
                for ann in annotation:
                    if isinstance(ann, GeneratingRule):
                        rule = ann

            if rule:
                value = RandomModelGenerator._generate_from_regex(rule.regex, actual_type)
            else:
                value = RandomModelGenerator._generate_value(actual_type)

            init_data[filed_name] = value

        return cls(**init_data)


    @staticmethod
    def _generate_value(field_type: type) -> Any:
        if field_type is str:
            return str(uuid.uuid4())[:8]
        if field_type is int:
            return random.randint(0, 1000)
        if field_type is float:
            return round(random.uniform(0, 100.0), 2)
        if field_type is bool:
            return random.choice([True, False])
        if field_type is datetime:
            return datetime.now() - timedelta(seconds=random.randint(0, 1000))
        if field_type is list:
            return [str(uuid.uuid4())[:8] for _ in range(random.randint(10, 50))]
        if isinstance(field_type, type):
            return RandomModelGenerator.generate(field_type)
        return None

    @staticmethod
    def _generate_from_regex(regex: Any, field_type: type) -> Any:
        generated = rstr.xeger(regex)
        if field_type is int:
            return int(generated)
        elif field_type is float:
            return float(generated)
        return generated
