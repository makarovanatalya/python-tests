import pytest

from src.main.classes.api_manager import ApiManager
from src.main.ui.pages.transfer_page import TransferPage


@pytest.mark.ui
class TestTransferMoney:
    def test_user_can_transfer_money(self, new_page, api_manager: ApiManager, user_session, user_account_with_money, prepare_receiver):
        amount = 100.0
        receiver_account, receiver_user_steps = prepare_receiver
        receiver_name = receiver_user_steps.get_profile().name
        sender_account_balance_before = api_manager.user_steps.get_account_by_id(user_account_with_money.id).balance

        TransferPage(new_page).open().fill_transfer_form(
            account_number=user_account_with_money.accountNumber,
            recipient_name=receiver_name,
            recipient_account_number=receiver_account.accountNumber,
            amount=str(amount)
        ).send_transfer_form()

        sender_account_balance_after = api_manager.user_steps.get_account_by_id(user_account_with_money.id).balance
        receiver_account_balance_after = receiver_user_steps.get_account_by_id(receiver_account.id).balance

        assert sender_account_balance_after == sender_account_balance_before - amount, "Balance for sender did not change on BE"
        assert receiver_account_balance_after == amount, "Wrong receiver account balance"

    @pytest.mark.parametrize(("args", "message", "context_manager"), [
        ({"account_number": None}, "Please fill all fields and confirm", False),
        ({"recipient_name": None}, "The recipient name does not match the registered name", True),
        ({"recipient_account_number": None}, "Please fill all fields and confirm", False),
        ({"amount": None}, "Please fill all fields and confirm", False),
        ({"amount": "-1"}, "Error: Invalid transfer: insufficient funds or invalid accounts", True),
        ({"checkbox": False}, "Please fill all fields and confirm", False),
    ])
    def test_user_can_not_transfer_money_with_invalid_form(
            self, new_page, api_manager: ApiManager, user_session, user_account_with_money,prepare_receiver, args, message, context_manager
    ):
        receiver_account, receiver_user_steps = prepare_receiver
        receiver_name = receiver_user_steps.get_profile().name
        sender_account_balance_before = api_manager.user_steps.get_account_by_id(user_account_with_money.id).balance

        form_fields = {
            "account_number": user_account_with_money.accountNumber,
            "recipient_name": receiver_name,
            "recipient_account_number": receiver_account.accountNumber,
            "amount": "100",
            "checkbox": True,
        }
        form_fields.update(args)
        TransferPage(new_page).open().fill_transfer_form(**form_fields).send_transfer_form(message, context_manager)

        sender_account_balance_after = api_manager.user_steps.get_account_by_id(user_account_with_money.id).balance
        receiver_account_balance_after = receiver_user_steps.get_account_by_id(receiver_account.id).balance

        assert sender_account_balance_after == sender_account_balance_before, "Balance for sender chenged on BE"
        assert receiver_account_balance_after == 0, "Receiver account balance changed"

