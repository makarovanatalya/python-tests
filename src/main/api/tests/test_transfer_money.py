import pytest
import requests


@pytest.mark.api
class TestTransferMoney:
    def test_transfer_money_to_another_user(self):
        # RECEIVER USER
        receiver_username = "user_for_tests2"
        receiver_password = "verysTRongPassword33$"

        # create account
        response = requests.post(
            "http://localhost:4111/api/v1/accounts", auth=(receiver_username, receiver_password))
        receiver_account_number = int(response.json()["id"])
        receiver_balance_before = float(response.json()["balance"])

        # SENDER USER
        sender_username = "user_for_tests"
        sender_password = "verysTRongPassword33$"
        transfer_amount = 100.12

        # create account
        response = requests.post(
            "http://localhost:4111/api/v1/accounts", auth=(sender_username, sender_password))
        sender_account_number = int(response.json()["id"])

        # deposit
        response = requests.post(
            "http://localhost:4111/api/v1/accounts/deposit", auth=(sender_username, sender_password),
            json={"id": sender_account_number, "balance": transfer_amount})
        sender_balance_before = float(response.json()["balance"])

        # transfer
        response = requests.post(
            "http://localhost:4111/api/v1/accounts/transfer", auth=(sender_username, sender_password),
            json={"senderAccountId": sender_account_number, "receiverAccountId": receiver_account_number, "amount": transfer_amount})

        response.raise_for_status()
        assert response.json()['amount'] == transfer_amount
        assert response.json()['message'] == "Transfer successful"

        # CHECK SENDERS ACCOUNT
        response = requests.get(
            "http://localhost:4111/api/v1/customer/accounts", auth=(sender_username, sender_password))

        sender_account = [acc for acc in response.json() if acc["id"] == sender_account_number]
        assert len(sender_account) == 1
        sender_account = sender_account[0]

        sender_balance = float(sender_account["balance"])
        assert sender_balance == sender_balance_before - transfer_amount

        # CHECK SENDERS TRANSACTIONS
        sender_transactions = sender_account["transactions"]
        transactions = sender_transactions[-1]
        assert transactions["amount"] == transfer_amount
        assert transactions["type"] == "TRANSFER_OUT"  # TODO: sometimes it's deposit, create function that gets last transaction

        # CHECK RECEIVER ACCOUNT
        response = requests.get(
            "http://localhost:4111/api/v1/customer/accounts", auth=(receiver_username, receiver_password))

        receiver_account = [acc for acc in response.json() if acc["id"] == receiver_account_number]
        assert len(receiver_account) == 1
        receiver_account = receiver_account[0]

        receiver_balance = float(receiver_account["balance"])
        assert receiver_balance == receiver_balance_before + transfer_amount

        # CHECK RECEIVER TRANSACTIONS
        receiver_transactions = receiver_account["transactions"]
        transactions = receiver_transactions[-1]
        assert transactions["amount"] == transfer_amount
        assert transactions[ "type"] == "TRANSFER_IN"


