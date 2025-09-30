from typing import List

from src.main.api.models.account import Account
from src.main.api.models.base_model import BaseModel


class Profile(BaseModel):
    accounts: List[Account]
    name: str
    username: str
    password: str
    role: str


class ProfileRequest(BaseModel):
    name: str


class ProfileResponse(BaseModel):
    customer: Profile
    message: str