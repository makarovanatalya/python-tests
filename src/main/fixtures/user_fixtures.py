import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user import CreateUserRequest, CreateUserResponse
from src.main.api.models.profile import ProfileRequest
from src.main.api.steps.user_steps import UserSteps
from src.main.classes.api_manager import ApiManager
from src.main.configs.config import Config


@pytest.fixture
def user_request(api_manager: ApiManager) -> CreateUserResponse:
    user_data = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_data)
    api_manager.user_steps.set_user(user_data)
    return user_data

@pytest.fixture
def user_account(api_manager: ApiManager, user_request: CreateUserRequest):
    return api_manager.user_steps.create_account()

@pytest.fixture
def user_account_with_money(api_manager: ApiManager, user_account):
    api_manager.user_steps.deposit_money(user_account.id, float(Config.get('maxDepositAmount')))
    return user_account

@pytest.fixture
def prepare_receiver(api_manager: ApiManager):
    receiver_user = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(receiver_user)
    receiver_user_steps = UserSteps(created_object=[]).set_user(receiver_user)
    receiver_user_steps.update_profile(ProfileRequest(name=RandomData.get_faker().name()))
    receiver_account = receiver_user_steps.create_account()
    return receiver_account, receiver_user_steps