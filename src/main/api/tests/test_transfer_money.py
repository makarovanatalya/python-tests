import pytest

from src.main.api.models.account import GetAccountsResponse
from src.main.api.models.create_account import CreateAccountResponse
from src.main.api.models.deposit_money import DepositMoneyResponse, DepositMoneyRequest
from src.main.api.models.transfer import TransferResponse, TransferRequest
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requester.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestTransferMoney:
    def test_transfer_money_to_another_user(self):
        # RECEIVER USER
        receiver_username = "user_for_tests2"
        receiver_password = "verysTRongPassword33$"

        # create account
        receiver_account: CreateAccountResponse = ValidatedCrudRequester(
            endpoint=Endpoint.CREATE_ACCOUNT,
            request_spec=RequestSpecs.user_auth_spec(receiver_username, receiver_password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(model=None)

        # SENDER USER
        sender_username = "user_for_tests"
        sender_password = "verysTRongPassword33$"
        transfer_amount = 100.12

        # create account
        sender_account: CreateAccountResponse = ValidatedCrudRequester(
            endpoint=Endpoint.CREATE_ACCOUNT,
            request_spec=RequestSpecs.user_auth_spec(sender_username, sender_password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(model=None)

        # deposit
        deposit_money_response : DepositMoneyResponse = ValidatedCrudRequester(
            endpoint=Endpoint.DEPOSIT_MONEY,
            request_spec=RequestSpecs.user_auth_spec(sender_username, sender_password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(model=DepositMoneyRequest(id=sender_account.id,balance=transfer_amount))
        assert deposit_money_response.balance == transfer_amount

        # transfer
        transfer_response: TransferResponse = ValidatedCrudRequester(
            endpoint=Endpoint.TRANSFER,
            request_spec=RequestSpecs.user_auth_spec(sender_username, sender_password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(model=TransferRequest(senderAccountId=sender_account.id, receiverAccountId=receiver_account.id, amount=transfer_amount))

        assert transfer_response.amount == transfer_amount
        assert transfer_response.message == "Transfer successful"

        # CHECK SENDERS ACCOUNT

        sender_accounts : GetAccountsResponse = ValidatedCrudRequester(
            endpoint=Endpoint.GET_ACCOUNTS,
            request_spec=RequestSpecs.user_auth_spec(sender_username, sender_password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()

        sender_account = [acc for acc in sender_accounts.root if acc.id == sender_account.id]
        assert len(sender_account) == 1
        sender_account = sender_account[0]

        assert sender_account.balance == deposit_money_response.balance - transfer_amount

        # CHECK SENDERS TRANSACTIONS
        sender_transaction = sender_account.transactions[-1] # TODO: sometimes it's deposit, create function that gets last transaction
        assert sender_transaction.amount == transfer_amount
        # assert sender_transaction.type == "TRANSFER_OUT"

        # CHECK RECEIVER ACCOUNT
        receiver_accounts : GetAccountsResponse = ValidatedCrudRequester(
            endpoint=Endpoint.GET_ACCOUNTS,
            request_spec=RequestSpecs.user_auth_spec(receiver_username, receiver_password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()

        receiver_account = [acc for acc in receiver_accounts.root if acc.id == receiver_account.id]
        assert len(receiver_account) == 1
        receiver_account = receiver_account[0]
        assert receiver_account.balance == transfer_amount

        # CHECK RECEIVERS TRANSACTIONS
        receiver_transaction = receiver_account.transactions[-1]
        assert receiver_transaction.amount == transfer_amount
        assert receiver_transaction.type == "TRANSFER_IN"
