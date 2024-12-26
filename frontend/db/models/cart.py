import ormar
from ..database import ormar_base_config


class Cart(ormar.Model):
    ormar_config = ormar_base_config.copy() 

    id: int = ormar.Integer(primary_key=True)
    user_id: int = ormar.ForeignKey("User")  # Связь с таблицей Users
    item_id: int = ormar.ForeignKey("Item")  # Связь с таблицей Items
    quantity: int = ormar.Integer(nullable=False)
