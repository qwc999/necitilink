import csv
from config.logger import logger
from db.models import Item, database, Category


async def load_items_to_db():
    # Открываем соединение с базой данных
    async with database.transaction():
        # Проверяем, пустая ли таблица
        count = await Item.objects.count()
        if count > 0:
            logger.info("Items already loaded") 
            return

        # Открываем CSV файл
        with open('items.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Создаём список объектов для вставки
            items_to_insert = []

            for row in reader:
                # Преобразуем данные из CSV в формат, подходящий для модели
                item = Item(
                    id=int(row['item_id']),
                    name=row['item_name'].strip(),
                    category_id=int(row['item_category_id']),
                    img="image.png"
                )
                items_to_insert.append(item)

            # Вставляем данные в таблицу
            await Item.objects.bulk_create(items_to_insert)


async def load_categories_to_db():
    # Открываем соединение с базой данных
    async with database.transaction():
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
                    id=int(row['item_category_id']),
                    name=row['item_category_name'].strip(),
                    subcategory=row['subcategory_id'].strip()
                )
                categories_to_insert.append(category)

            # Вставляем данные в таблицу
            await Category.objects.bulk_create(categories_to_insert)