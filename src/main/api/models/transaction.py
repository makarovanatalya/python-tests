from src.main.api.models.base_model import BaseModel


class Transaction(BaseModel):
    id: int
    amount: float
    type: str
    timestamp: str  # TODO: transform to timestamp?
    relatedAccountId: int
