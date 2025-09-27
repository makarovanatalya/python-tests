from typing import List, Optional

from pydantic import RootModel
from datetime import datetime

from src.main.api.models.base_model import BaseModel
from src.main.api.models.transaction import Transaction


class Account(BaseModel):
    id: int
    accountNumber: str
    balance: float
    transactions: List[Transaction]

    def get_last_transaction(self) -> Optional[Transaction]:
        if not self.transactions:
            return None
        last_transaction = self.transactions[0]
        for transaction in self.transactions:
            if last_transaction.id < transaction.id:
                last_transaction = transaction
        return last_transaction

class GetAccountsResponse(RootModel[List[Account]]): ...
