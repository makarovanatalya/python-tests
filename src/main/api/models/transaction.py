from enum import Enum

from src.main.api.models.base_model import BaseModel
from datetime import datetime
from pydantic import field_validator


class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    TRANSFER_OUT = "TRANSFER_OUT"
    TRANSFER_IN = "TRANSFER_IN"

class Transaction(BaseModel):
    id: int
    amount: float
    type: TransactionType
    timestamp: datetime  # Changed from str to datetime
    relatedAccountId: int

    @field_validator('timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, v):
        if isinstance(v, str):
            date_format = "%a %b %d %H:%M:%S %Z %Y"
            return datetime.strptime(v, date_format)
        return v
