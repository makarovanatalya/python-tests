import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_account import CreateAccountResponse
from src.main.api.models.create_user import CreateUserResponse
from src.main.api.models.transaction import TransactionType
from src.main.classes.api_manager import ApiManager
from src.main.configs.config import Config


def prepare_sender(api_manager: ApiManager, user_account: CreateAccountResponse, deposit_amount: float):
    max_deposit_amount = float(Config.get('maxDepositAmount'))
    while deposit_amount > 0:
        amount = max_deposit_amount if deposit_amount > max_deposit_amount else deposit_amount
        api_manager.user_steps.deposit_money(user_account.id, amount)
        deposit_amount -= amount
    return user_account

@pytest.mark.api
class TestTransferMoney:
    @pytest.mark.parametrize("transfer_amount", [
        RandomData.get_random_float(0,1),
        float(Config.get('maxTransferAmount'))
    ])
    def test_transfer_money_to_another_user(
            self,
            api_manager: ApiManager,
            user_request: CreateUserResponse,
            user_account: CreateAccountResponse,
            transfer_amount: float,
            prepare_receiver
    ):
        sender_account = prepare_sender(api_manager, user_account, transfer_amount)
        receiver_account, receiver_user_steps = prepare_receiver

        # TRANSFER
        api_manager.user_steps.transfer_money(
            sender_account_id=sender_account.id,
            receiver_account_id=receiver_account.id,
            amount=transfer_amount,
        )

        # CHECK SENDERS ACCOUNT & TRANSACTION
        sender_account = api_manager.user_steps.get_account_by_id(sender_account.id)
        assert sender_account.balance == 0, "Sender account balance did not change"

        sender_transaction = sender_account.get_last_transaction()
        assert sender_transaction.amount == transfer_amount, "Transfer amount is wrong in sender transaction"
        assert sender_transaction.type == TransactionType.TRANSFER_OUT, "Transfer transaction type is incorrect for sender account"

        # CHECK RECEIVER ACCOUNT & TRANSACTION
        receiver_account = receiver_user_steps.get_account_by_id(receiver_account.id)
        assert receiver_account.balance == transfer_amount, "Receiver account balance did not change"

        receiver_transaction = receiver_account.get_last_transaction()
        assert receiver_transaction.amount == transfer_amount, "Transfer amount is wrong in receiver transaction"
        assert receiver_transaction.type == TransactionType.TRANSFER_IN, "Transfer transaction type is incorrect for receiver account"

    def test_transfer_money_beyond_balance(
            self,
            api_manager: ApiManager,
            user_request: CreateUserResponse,
            user_account: CreateAccountResponse,
            prepare_receiver
        ):
        deposit_amount = 1000
        transfer_amount = deposit_amount + RandomData.get_random_float(1,10)
        sender_account = prepare_sender(api_manager, user_account, deposit_amount)
        receiver_account, receiver_user_steps = prepare_receiver

        api_manager.user_steps.transfer_money_incorrectly(
                sender_account_id=sender_account.id,
                receiver_account_id=receiver_account.id,
                amount=transfer_amount,
                error_text="Invalid transfer: insufficient funds or invalid accounts",
        )

    @pytest.mark.skip(reason="limits removed")
    def test_transfer_money_beyond_limit(
            self,
            api_manager: ApiManager,
            user_request: CreateUserResponse,
            user_account: CreateAccountResponse,
            prepare_receiver
        ):
        transfer_amount = float(Config.get('maxTransferAmount')) + RandomData.get_random_float(1,10)
        sender_account = prepare_sender(api_manager, user_account, transfer_amount)
        receiver_account, receiver_user_steps = prepare_receiver
        api_manager.user_steps.transfer_money_incorrectly(
                sender_account_id=sender_account.id,
                receiver_account_id=receiver_account.id,
                amount=transfer_amount,
                error_text="Transfer amount cannot exceed 10000",
        )

    def test_transfer_to_own_account(
            self,
            api_manager: ApiManager,
            user_request: CreateUserResponse,
            user_account: CreateAccountResponse,
        ):
        transfer_amount = RandomData.get_random_float(1, float(Config.get('maxTransferAmount')))
        sender_account = prepare_sender(api_manager, user_account, transfer_amount)
        receiver_account = api_manager.user_steps.create_account()
        api_manager.user_steps.transfer_money(sender_account.id, receiver_account.id, transfer_amount)

    def test_transfer_without_access_to_account(
            self,
            api_manager: ApiManager,
            user_request: CreateUserResponse,
            user_account: CreateAccountResponse,
            prepare_receiver
        ):
        transfer_amount = RandomData.get_random_float(1, float(Config.get('maxTransferAmount')))
        sender_account = prepare_sender(api_manager, user_account, transfer_amount)
        receiver_account, receiver_user_steps = prepare_receiver
        receiver_user_steps.transfer_money_incorrectly(
                sender_account_id=sender_account.id,
                receiver_account_id=receiver_account.id,
                amount=transfer_amount,
                error_text="Unauthorized access to account",
        )

