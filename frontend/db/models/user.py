import ormar
from ..database import ormar_base_config

#Описание
class User(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, nullable=False)
    email: str = ormar.String(max_length=100, unique=True, nullable=False)
    password_hash: str = ormar.String(max_length=255, nullable=False)