from typing import Optional, List

from pydantic import RootModel

from src.main.api.models.account import Account
from src.main.api.models.base_model import BaseModel


class User(BaseModel):
    id: int
    username: str
    password: str
    name: Optional[str] = None
    role: str
    accounts: List[Account]

class GetUsersResponse(RootModel[List[User]]): ...