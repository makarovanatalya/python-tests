import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user import CreateUserRequest, CreateUserResponse


@pytest.fixture
def user_request(api_manager: ApiManager) -> CreateUserResponse:
    user_data = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_data)
    api_manager.user_steps.set_user(user_data)
    return user_data

@pytest.fixture
def user_account(api_manager: ApiManager, user_request: CreateUserRequest):
    return api_manager.user_steps.create_account()
