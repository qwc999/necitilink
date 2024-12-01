from contextlib import asynccontextmanager
from fastapi import FastAPI
from faststream import FastStream
from faststream.kafka import KafkaBroker
from faststream.security import SASLPlaintext
from config.logger import logger
from config.settings import (
    KAFKA_URL,
    KAFKA_PASSWORD,
    KAFKA_USERNAME
)

# Отсюда 
security = SASLPlaintext(
    username=KAFKA_USERNAME,
    password=KAFKA_PASSWORD,
    use_ssl=False
)
broker = KafkaBroker(
    KAFKA_URL,
    security=security
    )
stream = FastStream(broker)
# до сюда не трогать

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Здесь прописывать код, который нужно запустить перед или после работы
        yield разделитель до и после

    Args:
        app (FastAPI)
    """
    await stream.start()
    logger.info("App started")
    yield
    await stream.stop()
    logger.info("App stopped")

app = FastAPI(lifespan=lifespan)


@app.post()
async def post_request(update: dict) -> None:
    """Пример отправления JSON в топик request

    Args:
        update (dict): JSON
    """
    await broker.publish(update, topic="request", partition=4)
