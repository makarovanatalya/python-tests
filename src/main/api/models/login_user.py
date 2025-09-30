from src.main.api.models.base_model import BaseModel


class LoginUserRequest(BaseModel):
    username: str
    password: str

class LoginUserResponse(BaseModel):
    username: str
    role: str
