import ormar
from ..database import ormar_base_config
from .category import Category  # Import the Category class


class Item(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=300, nullable=False)
    category_id: int = ormar.ForeignKey(Category)  # Связь с таблицей Categories
    price: int = ormar.Integer(default=100)
    img: str = ormar.String(max_length=255, nullable=True)