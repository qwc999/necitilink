import asyncio
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

app = FastStream(broker)
# до сюда не трогать

@broker.subscriber("request")
async def process_job(update: dict):
    """Пример реализации консьюмера с помощью декоратора subcriber

    Args:
        update (dict): JSON из топика request
    """
    pass


async def main():
    """Функция для запуска
    """
    await connect_to_db()
    await app.run()
    logger.info("App started")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.run(disconnect_from_db())
