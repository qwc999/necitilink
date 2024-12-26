"""Сюда не лезь"""

from alembic import context
from sqlalchemy import create_engine
from .database import ormar_base_config
from config.settings import DB_URL

config = context.config


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DB_URL,
        target_metadata=ormar_base_config.metadata,
        literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(DB_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=ormar_base_config.metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
