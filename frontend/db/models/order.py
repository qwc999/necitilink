import ormar
from datetime import datetime
from ..database import ormar_base_config
from .user import User  # Import the User class

class Order(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id: int = ormar.Integer(primary_key=True)
    user_id: int = ormar.ForeignKey(User)  # Связь с таблицей Users
    total_amount: float = ormar.Float(nullable=False)
    order_date: datetime = ormar.DateTime(default=datetime.now)
    status: str = ormar.String(max_length=50, default="not paid")
