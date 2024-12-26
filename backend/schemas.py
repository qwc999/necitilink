# Определение схемы для регистрации пользователя
from pydantic import BaseModel


class UserRegister(BaseModel):
    name: str
    email: str
    password: str

# Определение схемы для авторизации пользователя
class UserLogin(BaseModel):
    email: str
    password: str

class Message(BaseModel):
    message: str
    user_id: int