# type: ignore
from __future__ import annotations

from alembic import context
from spellbot.models import Base, import_models
from sqlalchemy import engine_from_config, pool

import_models()
config = context.config
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an Engine
    is acceptable here as well.  By skipping the Engine creation we don't even need a
    DBAPI to be available. Calls to context.execute() here emit the given string to
    the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    is_sqlite = url.startswith("sqlite:")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        render_as_batch=is_sqlite,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a
    connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
