import csv
from config.logger import logger
from db.models import Item, Category
from db.database import ormar_base_config


async def load_items_to_db_in_batches(items, batch_size=1000):
    """
    Загрузка записей в таблицу Item батчами.

    :param items: Список объектов Item для загрузки.
    :param batch_size: Размер одного батча.
    """
    total_items = len(items)
    for i in range(0, total_items, batch_size):
        batch = items[i:i + batch_size]
        await Item.objects.bulk_create(batch)
        logger.info(f"Загружено {min(i + batch_size, total_items)} из {total_items} записей.")

async def load_items_to_db():
    """
    Основная функция загрузки данных из items.csv в базу.
    """
    async with ormar_base_config.database.transaction():
        count = await Item.objects.count()
        if count > 0:
            logger.info("Items already loaded") 
            return

        with open('items.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            items_to_insert = []

            for row in reader:
                item = Item(
                    id=int(row['item_id']),
                    name=row['item_name'].strip(),
                    category_id=int(row['item_category_id']) + 1,
                    img="image.png"
                )
                items_to_insert.append(item)

            # Загрузка данных батчами
            await load_items_to_db_in_batches(items_to_insert)


async def load_categories_to_db():
    # Открываем соединение с базой данных
    async with ormar_base_config.database.transaction():
        # Проверяем, пустая ли таблица
        count = await Category.objects.count()
        if count > 0:
            logger.info("Categories already loaded")
            return

        # Открываем CSV файл
        with open('item_categories.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Создаём список объектов для вставки
            categories_to_insert = []

            for row in reader:
                # Преобразуем данные из CSV в формат, подходящий для модели

                category = Category(
                    id=int(row['item_category_id']) + 1,
                    name=row['item_category_name'].strip(),
                    subcategory_id=row['subcategory_id'].strip()
                )
                categories_to_insert.append(category)

            # Вставляем данные в таблицу
            await Category.objects.bulk_create(categories_to_insert)