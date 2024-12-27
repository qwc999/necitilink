#Добавление товара в корзину
from fastapi import HTTPException
from db.models.cart import Cart
from db.models.item import Item


async def add_to_cart(user_id: int, item_id: int, quantity: int = 1):

    # Проверка, есть ли уже такой товар в корзине пользователя
    cart_item = await Cart.objects.filter(user_id=user_id, item_id=item_id).first()

    if cart_item:
        # Если товар уже есть в корзине, обновляем количество
        cart_item.quantity += quantity
        await cart_item.update()
    else:
        # Если товара нет в корзине, добавляем его
        cart_item = await Cart.objects.create(
            user_id=user_id,
            item_id=item_id,
            quantity=quantity,
        )

    return {"message": "Item added to cart successfully", "cart_item_id": cart_item.id}


#Удаление товара из корзины
async def delete_from_cart(user_id: int, item_id: int):
    # Проверка, существует ли запись в корзине для указанного пользователя и товара
    cart_item = await Cart.objects.filter(user_id=user_id, item_id=item_id).first()

    # Если запись не найдена, возвращаем ошибку
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    # Удаляем запись из корзины
    await cart_item.delete()

    # Возвращаем сообщение об успешном удалении
    return {"message": "Item removed from cart successfully"}


#Список товаров в корзине
async def get_cart_by_user(user_id: int):
   
    # Получаем все записи из корзины для указанного пользователя
    cart_items = await Cart.objects.filter(user_id=user_id).all()

    # Создаём список товаров с их количеством и деталями
    cart_details = []
    for cart_item in cart_items:
        item = await Item.objects.get(id=cart_item.item_id)
        cart_details.append({
            "item_id": item.id,
            "name": item.name,
            "price": item.price,
            "img": item.img,
            "quantity": cart_item.quantity,
        })

    # Возвращаем список товаров в корзине
    return {"user_id": user_id, "cart": cart_details}
