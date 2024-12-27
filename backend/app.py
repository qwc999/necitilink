import asyncio
from contextlib import asynccontextmanager
from http.client import HTTPException
from db.models.item import Item
from db.models.user import User
from db.operations.user import hash_password
from fastapi import FastAPI
from faststream import FastStream
from faststream.kafka import KafkaBroker, KafkaMessage
from faststream.kafka.security import SASLPlaintext
from config.logger import logger
from config.settings import (
    KAFKA_PASSWORD,
    KAFKA_URL,
    KAFKA_USERNAME
)
from db.models import Item, Cart, User
from db.connection import connect_to_db, disconnect_from_db
from db.operations import load_items_to_db, load_categories_to_db
from s3.operations import load_images_to_s3
from schemas import ItemToCart, ResponceAfterAuth, UserLogin, UserRegister


# Код отсюда
security = SASLPlaintext(
    username=KAFKA_USERNAME,
    password=KAFKA_PASSWORD,
    use_ssl=False
)
broker = KafkaBroker(
    KAFKA_URL,
    security=security
    )

kafka_client = FastStream(broker)
# до сюда не трогать

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Здесь прописывать код, который нужно запустить перед или после работы
        yield разделитель до и после

    Args:
        app (FastAPI)
    """
    await kafka_client.start()
    await load_images_to_s3()
    await connect_to_db()
    await load_categories_to_db()   
    await load_items_to_db()
    logger.info("App started")
    yield
    await kafka_client.stop()
    await disconnect_from_db()
    logger.info("App stopped")

app = FastAPI(lifespan=lifespan)


@app.post("/login", response_model=UserLogin)
async def login(user: UserLogin):
    # Поиск пользователя по email
    existing_user = await User.objects.filter(email=user.email).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")

    # Проверка пароля
    if hash_password(user.password) != existing_user.password_hash:
        raise HTTPException(status_code=400, detail="Incorrect password")

    # Возвращаем успешный ответ
    return ResponceAfterAuth(message="Login successful", user_id=existing_user.id)

@app.post("/register", response_model=UserRegister)
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
    return ResponceAfterAuth(message="User registered successfully", user_id=new_user.id)

@broker.subscriber("add_to_list")
async def process_job(row: dict):
    """Пример реализации консьюмера с помощью декоратора subcriber

    Args:
        update (dict): JSON из топика request
    """
    try:
        update = ItemToCart(**row)
    except Exception as e:
        logger.error(e, exc_info=True)
        return
    new_item = update.item
    user = await User.objects.get(
            id=update.user_id
            )
    user_cart = await Cart.objects.get_or_none(
        user_id=user,
        item_id=new_item.id
        )
    if user_cart:
        user_cart(quantity=user_cart.quantity + 1)
    else:
        await Cart.objects.create(
            user_id=user,
            item_id=new_item.id,
            quantity=1
        )
        logger.info(f"Add item ({new_item.id}) to user ({user.id}) cart")
