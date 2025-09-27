import pytest

from src.main.api.models.profile import ProfileResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requester.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestDepositMoney:
    def test_deposit_money(self):
        user_name = "user_for_tests"
        password = "verysTRongPassword33$"
        name = "lalala la"

        # CHANGE NAME
        change_name_request : ProfileResponse = ValidatedCrudRequester(
            endpoint=Endpoint.UPDATE_PROFILE,
            request_spec=RequestSpecs.user_auth_spec(user_name, password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()

        assert change_name_request.name == name

        get_profile_request : ProfileResponse = ValidatedCrudRequester(
            endpoint=Endpoint.UPDATE_PROFILE,
            request_spec=RequestSpecs.user_auth_spec(user_name, password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()

        assert get_profile_request.name == name
