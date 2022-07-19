import os

from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    WRITER_DB_URL: str = f"postgresql+asyncpg://user:password@localhost:5432/db_name"
    READER_DB_URL: str = f"postgresql+asyncpg://user:password@localhost:5432/db_name"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = f"postgresql+asyncpg://user:password@localhost:5432/db_name"
    READER_DB_URL: str = f"postgresql+asyncpg://user:password@localhost:5432/db_name"


class LocalConfig(Config):
    WRITER_DB_URL: str = f"postgresql+asyncpg://user:password@localhost:5432/db_name"
    READER_DB_URL: str = f"postgresql+asyncpg://user:password@localhost:5432/db_name"


class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = f"postgresql+asyncpg://user:password@localhost:5432/db_name"
    READER_DB_URL: str = f"postgresql+asyncpg://user:password@localhost:5432/db_name"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "development": DevelopmentConfig(),
        "local": LocalConfig(),
        "production": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
