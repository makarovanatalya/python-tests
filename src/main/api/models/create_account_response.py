from typing import List, Dict

from src.main.api.models.base_model import BaseModel

class CreateAccountResponse(BaseModel):
    id: int
    accountNumber: str
    balance: float
    transactions: List[Dict[str, str]]
