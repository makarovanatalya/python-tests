import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account import CreateAccountResponse
from src.main.api.models.create_user import CreateUserResponse
from src.main.api.models.transaction import TransactionType


# cases:
# deposit to own account
# deposit to account of another user
# deposit to account that doesn't exist

@pytest.mark.api
class TestDepositMoney:
    def test_deposit_money(self,  api_manager: ApiManager, user_request: CreateUserResponse, user_account: CreateAccountResponse):
        deposit_amount = 100.01

        deposit_response = api_manager.user_steps.deposit_money(user_request.username, user_request.password, user_account.id,deposit_amount)
        assert user_account.balance + deposit_amount == deposit_response.balance, "Wrong balance after deposit"

        account = api_manager.user_steps.get_account_by_id(user_request.username, user_request.password, user_account.id)
        assert account.balance == user_account.balance + deposit_amount

        last_transaction = account.get_last_transaction()
        assert last_transaction.amount == deposit_amount
        assert last_transaction.type == TransactionType.DEPOSIT
