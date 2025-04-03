import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, create_engine
from sqlalchemy.exc import OperationalError
from alembic import context
from dotenv import load_dotenv

from src.app.base.infrastructure.model.base_model import Base
from src.config.models import *  # assure-toi que ça importe tous tes modèles

# Alembic config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Charger les variables d'environnement
load_dotenv()

# Construire l'URL de la base depuis les variables d'env
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("POSTGRES_DB")

database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Injecter dans la config Alembic
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
else:
    raise Exception("❌ Impossible de construire l'URL de la base de données.")

# ✅ Tester la connexion à la base
try:
    test_engine = create_engine(database_url)
    print("✅ Connexion à la base réussie.")
except OperationalError as e:
    print("❌ Connexion à la base échouée :", str(e))
    raise

# Définir les métadonnées pour Alembic
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
