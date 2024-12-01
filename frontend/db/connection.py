from config.logger import logger
from .database import ormar_base_config


async def connect_to_db():
    ormar_base_config.metadata.create_all(ormar_base_config.engine)
    if not ormar_base_config.database.is_connected:
        await ormar_base_config.database.connect()


async def disconnect_from_db():
    if ormar_base_config.database.is_connected:
        await ormar_base_config.database.disconnect()
    logger.info("Disconnect from database")
