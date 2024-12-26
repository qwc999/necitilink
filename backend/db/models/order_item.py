import ormar
from ..database import ormar_base_config

class OrderItem(ormar.Model):
    ormar_config = ormar_base_config.copy()  

    id: int = ormar.Integer(primary_key=True)
    order_id: int = ormar.ForeignKey("Order")  # Связь с таблицей Orders
    item_id: int = ormar.ForeignKey("Item")    # Связь с таблицей Items
    quantity: int = ormar.Integer(nullable=False)
    price: float = ormar.Float(nullable=False)
