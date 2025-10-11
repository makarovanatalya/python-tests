from typing import Annotated
from typing import Optional, List, Dict

from src.main.api.configs.config import Config
from src.main.api.generators.generating_rule import GeneratingRule
from src.main.api.models.base_model import BaseModel


class CreateUserRequest(BaseModel):
    username: Annotated[str, GeneratingRule(regex=r"^[a-zA-Z0-9]{3,15}$")]
    password: Annotated[str, GeneratingRule(regex=r"^[A-Z]{3}[a-z]{4}[0-9]{3}[!@#$%^&=+]{3}$")]
    role: Annotated[str, GeneratingRule(regex=r"^USER$")]

    @staticmethod
    def get_admin():
        return CreateUserRequest(username=Config.get('admin_account'), password=Config.get('admin_password'), role="ADMIN")


class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    name: Optional[str] = None
    role: str
    accounts: List[Dict[str, str]]