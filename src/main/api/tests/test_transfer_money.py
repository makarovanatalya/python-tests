import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_account import CreateAccountResponse
from src.main.api.models.create_user import CreateUserResponse, CreateUserRequest
from src.main.api.models.transaction import TransactionType
from src.main.api.steps.user_steps import UserSteps


@pytest.mark.api
class TestTransferMoney:
    @pytest.mark.parametrize("transfer_amount", [0.0000001, 5000])
    def test_transfer_money_to_another_user(
            self, api_manager: ApiManager, user_request: CreateUserResponse, user_account: CreateAccountResponse, transfer_amount: float
    ):
        # SENDER USER PREPARATION
        sender_account = user_account
        deposit_response = api_manager.user_steps.deposit_money(sender_account.id, transfer_amount)

        # RECEIVER USER PREPARATION
        receiver_user =RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(receiver_user)
        receiver_user_steps = UserSteps(created_object=[]).set_user(receiver_user)
        receiver_user_steps.login()
        receiver_account = receiver_user_steps.create_account()

        # TRANSFER
        api_manager.user_steps.transfer_money(
            sender_account_id=sender_account.id,
            receiver_account_id=receiver_account.id,
            amount=transfer_amount,
        )

        # CHECK SENDERS ACCOUNT & TRANSACTION
        sender_account = api_manager.user_steps.get_account_by_id(sender_account.id)
        assert sender_account.balance == deposit_response.balance - transfer_amount, "Sender account balance did not change"

        sender_transaction = sender_account.get_last_transaction()
        assert sender_transaction.amount == transfer_amount, "Transfer amount is wrong in sender transaction"
        assert sender_transaction.type == TransactionType.TRANSFER_OUT, "Transfer transaction type is incorrect for sender account"

        # CHECK RECEIVER ACCOUNT & TRANSACTION
        receiver_account = receiver_user_steps.get_account_by_id(receiver_account.id)
        assert receiver_account.balance == transfer_amount, "Receiver account balance did not change"

        receiver_transaction = receiver_account.get_last_transaction()
        assert receiver_transaction.amount == transfer_amount, "Transfer amount is wrong in receiver transaction"
        assert receiver_transaction.type == TransactionType.TRANSFER_IN, "Transfer transaction type is incorrect for receiver account"
