from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 1. Import your Base and models
from app.db.database import Base
from app.db import models  

# 2. Set your DB URL 
from app.db.database import DB_URL
config = context.config
config.set_main_option("sqlalchemy.url", DB_URL)

# 3. Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. Set target metadata
target_metadata = Base.metadata

# 5. Migration methods (unchanged)
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
