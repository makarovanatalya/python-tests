from src.main.api.models.comparasion.model_assertions import ModelAssertions
from src.main.api.models.create_user import CreateUserRequest, CreateUserResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requester.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requester.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
import allure


class AdminSteps(BaseSteps):
    @allure.step
    def create_user(self, user_request: CreateUserRequest) -> CreateUserResponse:
        create_user_response: CreateUserResponse = ValidatedCrudRequester(
            endpoint=Endpoint.ADMIN_CREATE_USER,
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.entity_was_created(),
        ).post(user_request)
        ModelAssertions(user_request, create_user_response).match()

        self.created_objects.append(create_user_response)
        return create_user_response

    @allure.step
    def create_invalid_user(self, user_request: CreateUserRequest, error_key: str, error_value: str):
        CrudRequester(
            endpoint=Endpoint.ADMIN_CREATE_USER,
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.request_returns_bad_request(error_key, error_value),
        ).post(user_request)


    @allure.step
    def delete_user(self, user_id: int) -> None:
        CrudRequester(
            endpoint=Endpoint.ADMIN_DELETE_USER,
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.entity_was_deleted(),
        ).delete(user_id)

    @allure.step
    def get_users(self):
        return ValidatedCrudRequester(
            endpoint=Endpoint.ADMIN_GET_USERS,
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.request_returns_ok(),
        ).get().root

    @allure.step
    def get_user_by_username(self, username: str):
        users = self.get_users()
        user = [user for user in users if user.username == username]
        return user[0] if user else None
