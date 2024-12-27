import asyncio
from contextlib import asynccontextmanager
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
from db.connection import connect_to_db, disconnect_from_db
from db.operations import load_items_to_db, load_categories_to_db
from s3.operations import load_images_to_s3


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


@broker.subscriber("request")
async def process_job(update: dict):
    """Пример реализации консьюмера с помощью декоратора subcriber

    Args:
        update (dict): JSON из топика request
    """
    pass
