from typing import List, Optional

from src.main.api.models.account import Account
from src.main.api.models.base_model import BaseModel


class Profile(BaseModel):
    accounts: List[Account]
    name: Optional[str]
    username: str
    password: str
    role: str


class ProfileRequest(BaseModel):
    name: str


class ProfileResponse(BaseModel):
    customer: Profile
    message: str