import pytest
import requests


@pytest.mark.api
class TestDepositMoney:
    def test_deposit_money(self):
        user_name = "user_for_tests"
        password = "verysTRongPassword33$"
        name = "lalala la"

        # CHANGE NAME
        response = requests.put("http://localhost:4111/api/v1/customer/profile", auth=(user_name, password), json={"name": name})
        assert response.json()['customer']['name'] == name

        # CHECK PROFILE
        response = requests.get("http://localhost:4111/api/v1/customer/profile", auth=(user_name, password))
        name_after= response.json()['name']
        assert name_after == name
