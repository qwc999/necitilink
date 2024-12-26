import ormar
from ..database import ormar_base_config


class Category(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100, unique=True, nullable=False)
    subcategory_id: int = ormar.Integer(nullable=False) 
