# Определение схемы для регистрации пользователя
from pydantic import BaseModel

from db.models.item import Item


class UserRegister(BaseModel):
    name: str
    email: str
    password: str

# Определение схемы для авторизации пользователя
class UserLogin(BaseModel):
    email: str
    password: str

class ResponceAfterAuth(BaseModel):
    message: str
    user_id: int
    
class ItemToCart(BaseModel):
    item: Item
    user_id: int