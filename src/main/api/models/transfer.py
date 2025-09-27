from src.main.api.models.base_model import BaseModel


class TransferRequest(BaseModel):
    senderAccountId: int
    receiverAccountId: int
    amount: float


class TransferResponse(BaseModel):
    message: str
    senderAccountId: int
    receiverAccountId: int
    amount: float
