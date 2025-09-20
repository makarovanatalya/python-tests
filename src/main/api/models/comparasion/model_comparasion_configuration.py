import logging
from pathlib import Path
import configparser
from typing import List, Dict, Type, Optional


class ComparisonRule:
    def __init__(self, response_class_name: str, field_pairs: List[str]):
        self._response_class_name = response_class_name
        self.field_pairs = field_pairs
        self._field_mapping: Dict[str, str] = {}

        for pair in self.field_pairs:
            parts = pair.split('=')
            if len(parts) == 2:
                self._field_mapping[parts[0].strip()] = parts[1].strip()
            else:
                logging.warning(f'Invalid pair: {pair}')
                self._field_mapping[pair.strip()] = pair.strip()

    @property
    def response_class_name(self) -> str:
        return self._response_class_name

    @property
    def field_mapping(self) -> Dict[str, str]:
        return self._field_mapping


class ModelComparasionConfigLoader:
    def __init__(self, config_file: str):
        self.rules: Dict[str, ComparisonRule] = {}
        self._load_config(config_file)

    def _load_config(self, config_file: str):
        config_path = Path(__file__).parents[5] / 'resources' / config_file
        if not config_path.exists():
            raise ImportError(f'Config file not found: {config_path}')
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(config_path)

        for key in config.defaults():
            value = config.defaults()[key]
            target = value.split(':')
            if len(target) != 2:
                continue

            response_class = target[0].strip()
            field_list = [field.strip() for field in target[1].split(',')]

            self.rules[key.strip()] = ComparisonRule(response_class, field_list)

    def get_rule_for(self, request_class: Type) -> Optional[ComparisonRule]:
        return self.rules.get(request_class.__class__.__name__)
