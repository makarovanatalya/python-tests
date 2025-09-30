from src.main.api.models.account import Account
from src.main.api.models.base_model import BaseModel


class DepositMoneyRequest(BaseModel):
    id: int
    balance: float


class DepositMoneyResponse(Account): ...
