import hashlib
from pydantic import BaseModel

from db.models import User
from fastapi import HTTPException

from ...schemas import UserRegister, UserLogin, Message
    
    

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

#Регистрация пользователя
async def register(user: UserRegister):
    # Проверка, существует ли пользователь с таким email
    existing_user = await User.objects.filter(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Создание нового пользователя
    new_user = await User.objects.create(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
    )
    return Message(message="User registered successfully", user_id=new_user.id)


#Авторизация пользователя
async def login(user: UserLogin):
    # Поиск пользователя по email
    existing_user = await User.objects.filter(email=user.email).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")

    # Проверка пароля
    if hash_password(user.password) != existing_user.password_hash:
        raise HTTPException(status_code=400, detail="Incorrect password")

    # Возвращаем успешный ответ
    return Message(message="Login successful", user_id=existing_user.id)