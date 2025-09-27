from typing import List

from pydantic import RootModel

from src.main.api.models.base_model import BaseModel
from src.main.api.models.transaction import Transaction


class Account(BaseModel):
    id: int
    accountNumber: str
    balance: float
    transactions: List[Transaction]

class GetAccountsResponse(RootModel[List[Account]]): ...
