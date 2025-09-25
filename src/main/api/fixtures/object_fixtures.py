import logging
from typing import List, Any

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user import CreateUserResponse


def cleanup_objects(objects: List[Any]) -> None:
    api_manager = ApiManager(objects)
    for obj in objects:
        if isinstance(obj, CreateUserResponse):
            api_manager.admin_steps.delete_user(obj.id)
        else:
            logging.warning(f"Object {obj.id} was not deleted")

@pytest.fixture()
def created_objects():
    objects: List[Any] = []
    yield objects
    cleanup_objects(objects)
