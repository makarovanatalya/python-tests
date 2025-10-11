import re

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user import CreateUserRequest


@pytest.mark.ui
class TestCreateAccount:
    def test_user_can_create_account(self, new_context, new_page, api_manager: ApiManager):
        new_user: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(new_user)
        auth_token = api_manager.user_steps.set_user(new_user).get_auth_token()

        script = "window.localStorage.setItem('authToken', '" + auth_token + "');"

        new_context.add_init_script(script)

        new_page.goto("/dashboard")

        create_account_button = new_page.get_by_role("button", name="Create New Account")
        create_account_button.wait_for(state="visible")


        with new_page.expect_event("dialog") as dialog:
            create_account_button.click()
            assert "New Account Created! Account Number:" in dialog.value.message

            account_number = None
            match = re.search(r"Account Number: (\w+)", dialog.value.message)
            if match:
                account_number = match.group(1)
            assert account_number, "Could not extract account number"

            dialog.value.accept()

        accounts = api_manager.user_steps.get_accounts().root
        assert len(accounts) == 1, "Wrong number of accounts returned"

        new_account = [acc for acc in accounts if acc.accountNumber == account_number]
        assert new_account, "Could find new account on BE"




