import pytest

from src.main.api.models.account import GetAccountsResponse
from src.main.api.models.create_account import CreateAccountResponse
from src.main.api.models.deposit_money import DepositMoneyRequest, DepositMoneyResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requester.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


# cases:
# deposit to own account
# deposit to account of another user
# deposit to account that doesn't exist

@pytest.mark.api
class TestDepositMoney:
    def test_deposit_money(self):
        user_name = "user_for_tests"
        password = "verysTRongPassword33$"
        balance_diff = 100.01

        # create account
        create_account_response : CreateAccountResponse = ValidatedCrudRequester(
            endpoint=Endpoint.CREATE_ACCOUNT,
            request_spec=RequestSpecs.user_auth_spec(user_name, password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(model=None)

        # deposit
        deposit_money_request : DepositMoneyRequest = DepositMoneyRequest(
            id=create_account_response.id,
            balance=balance_diff
        )
        deposit_money_response : DepositMoneyResponse = ValidatedCrudRequester(
            endpoint=Endpoint.DEPOSIT_MONEY,
            request_spec=RequestSpecs.user_auth_spec(user_name, password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(model=deposit_money_request)

        assert deposit_money_response.balance - create_account_response.balance == balance_diff

        # check that balance really changed
        get_accounts_response : GetAccountsResponse = ValidatedCrudRequester(
            endpoint=Endpoint.GET_ACCOUNTS,
            request_spec=RequestSpecs.user_auth_spec(user_name, password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()

        account = [acc for acc in get_accounts_response.root if acc.id == create_account_response.id]
        assert len(account) == 1
        account = account[0]

        assert account.balance == create_account_response.balance + balance_diff

        assert len(account.transactions) == len(create_account_response.transactions) + 1
        transaction = account.transactions[-1]
        assert transaction.amount == balance_diff
        assert transaction.type == "DEPOSIT"
