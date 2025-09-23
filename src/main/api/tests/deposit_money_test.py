import pytest
import requests


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
        response = requests.post(
            "http://localhost:4111/api/v1/accounts", auth=(user_name, password))
        account_number = response.json()["id"]
        balance_before = float(response.json()["balance"])
        transaction_count_before = len(response.json()["transactions"])

        # deposit
        response = requests.post(
            "http://localhost:4111/api/v1/accounts/deposit", auth=(user_name, password),
        json={"id": account_number, "balance": balance_diff})
        balance_after = float(response.json()["balance"])

        assert balance_after - balance_before == balance_diff

        # check that balance really changed
        response = requests.get(
            "http://localhost:4111/api/v1/customer/accounts", auth=(user_name, password))

        account = [acc for acc in response.json() if acc["id"] == account_number]
        assert len(account) == 1
        account = account[0]

        balance = float(account["balance"])
        assert balance == balance_after

        # check there's transaction
        transactions = account["transactions"]
        assert len(transactions) == transaction_count_before + 1
        transactions = transactions[-1]
        assert transactions["amount"] == balance_diff
        assert transactions["type"] == "DEPOSIT"
