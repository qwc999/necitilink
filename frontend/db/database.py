import databases
import ormar
import sqlalchemy

from config.settings import DB_URL

ormar_base_config = ormar.OrmarConfig(
    database=databases.Database(DB_URL),
    metadata=sqlalchemy.MetaData(),
    engine=sqlalchemy.create_engine(DB_URL),
)
