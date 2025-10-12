import pytest

from src.main.classes.api_manager import ApiManager
from src.main.configs.config import Config
from src.main.api.generators.random_data import RandomData
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_account import CreateAccountResponse
from src.main.api.models.create_user import CreateUserResponse, CreateUserRequest
from src.main.api.models.transaction import TransactionType
from src.main.api.steps.user_steps import UserSteps

DEFAULT_TRANSFER_AMOUNT = RandomData.get_random_float(1, float(Config.get('maxDepositAmount')))

@pytest.mark.api
class TestDepositMoney:
    @pytest.mark.parametrize("amount", [0.000001, float(Config.get('maxDepositAmount'))])
    def test_deposit_money(
            self,  api_manager: ApiManager, user_request: CreateUserResponse, user_account: CreateAccountResponse, amount: float
    ) -> None:
        deposit_response = api_manager.user_steps.deposit_money(user_account.id, amount)
        assert user_account.balance + amount == deposit_response.balance, "Wrong balance after deposit"

        account = api_manager.user_steps.get_account_by_id(user_account.id)
        assert account.balance == user_account.balance + amount

        last_transaction = account.get_last_transaction()
        assert last_transaction.amount == amount
        assert last_transaction.type == TransactionType.DEPOSIT

    def test_deposit_money_to_another_user_account(
            self,  api_manager: ApiManager, user_request: CreateUserResponse, user_account: CreateAccountResponse
    ) -> None:
        receiver_user = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(receiver_user)
        receiver_user_steps = UserSteps(created_object=[]).set_user(receiver_user)
        receiver_account = receiver_user_steps.create_account()

        api_manager.user_steps.deposit_money_incorrectly(receiver_account.id, DEFAULT_TRANSFER_AMOUNT, "Unauthorized access to account")
        assert_text = "Receiver user balance changed"
        assert receiver_account.balance == receiver_user_steps.get_account_by_id(receiver_account.id).balance, assert_text

    def test_deposit_money_to_non_existent_account(self, api_manager: ApiManager, user_request: CreateUserResponse) -> None:
        api_manager.user_steps.deposit_money_incorrectly(
            RandomData.get_faker().random_digit(),
            DEFAULT_TRANSFER_AMOUNT,
            "Unauthorized access to account"
        )

    @pytest.mark.parametrize("amount", [0, -1])
    def test_deposit_invalid_amount(
            self, api_manager: ApiManager, user_request: CreateUserRequest, user_account: CreateAccountResponse, amount: float
    ) -> None:
        api_manager.user_steps.deposit_money_incorrectly(user_account.id, amount, "Invalid account or amount")
        assert user_account.balance == api_manager.user_steps.get_account_by_id(user_account.id).balance, "Balance changed"

    def test_deposit_beyond_limit(
            self, api_manager: ApiManager, user_request: CreateUserRequest, user_account: CreateAccountResponse
    ) -> None:
        api_manager.user_steps.deposit_money_incorrectly(
            user_account.id,
            float(Config.get('maxDepositAmount')) + RandomData.get_random_float(0, 1),
            "Deposit amount exceeds the 5000 limit"
        )
        assert user_account.balance == api_manager.user_steps.get_account_by_id(user_account.id).balance, "Balance changed"
