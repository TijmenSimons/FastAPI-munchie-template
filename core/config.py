import os
from dotenv import load_dotenv
from pydantic import BaseSettings


# Check if environment variables are present if not we make use of the .env file to load them
if os.getenv("DU") is None:
    load_dotenv()


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    WRITER_DB_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:3301/mealmatch"
    )
    READER_DB_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:3301/mealmatch"
    )
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    AZURE_BLOB_ACCOUNT_URL: str = os.getenv("AZURE_BLOB_ACCOUNT_URL")
    IMAGE_CONTAINER_NAME: str = os.getenv("IMAGE_CONTAINER_NAME")
    AZURE_BLOB_CONNECTION_STRING: str = os.getenv("AZURE_BLOB_CONNECTION_STRING")
    AZURE_IMAGE_URL_BASE: str = os.getenv("AZURE_IMAGE_URL_BASE")
    OBJECT_STORAGE_INTERFACE: str = "azure"
    IMAGE_MAX_SIZE = 5 * 1024 * 1024  # 5 MB
    ACCESS_TOKEN_EXPIRE_PERIOD: int = 3600
    REFRESH_TOKEN_EXPIRE_PERIOD: int = 3600 * 24
    TASK_CAPTURE_EXCEPTIONS: bool = os.getenv("TASK_CAPTURE_EXCEPTIONS")
    SWIPE_SESSION_RECIPE_QUEUE: int = 5


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = f"postgresql+asyncpg://{os.getenv('DU')}:{os.getenv('DP')}@{os.getenv('H')}:{os.getenv('P')}/{os.getenv('DB')}"
    READER_DB_URL: str = f"postgresql+asyncpg://{os.getenv('DU')}:{os.getenv('DP')}@{os.getenv('H')}:{os.getenv('P')}/{os.getenv('DB')}"
    AZURE_BLOB_ACCOUNT_URL: str = os.getenv("AZURE_BLOB_ACCOUNT_URL")
    IMAGE_CONTAINER_NAME: str = os.getenv("IMAGE_CONTAINER_NAME")
    AZURE_BLOB_CONNECTION_STRING: str = os.getenv("AZURE_BLOB_CONNECTION_STRING")
    ACCESS_TOKEN_EXPIRE_PERIOD: int = os.getenv("ACCESS_TOKEN_EXPIRE_PERIOD")
    REFRESH_TOKEN_EXPIRE_PERIOD: int = os.getenv("REFRESH_TOKEN_EXPIRE_PERIOD")

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    WRITER_DB_URL: str = f"postgresql+asyncpg://{os.getenv('DU')}:{os.getenv('DP')}@{os.getenv('H')}:{os.getenv('P')}/{os.getenv('DB')}"
    READER_DB_URL: str = f"postgresql+asyncpg://{os.getenv('DU')}:{os.getenv('DP')}@{os.getenv('H')}:{os.getenv('P')}/{os.getenv('DB')}"
    AZURE_BLOB_ACCOUNT_URL: str = os.getenv("AZURE_BLOB_ACCOUNT_URL")
    IMAGE_CONTAINER_NAME: str = os.getenv("IMAGE_CONTAINER_NAME")
    AZURE_BLOB_CONNECTION_STRING: str = os.getenv("AZURE_BLOB_CONNECTION_STRING")
    ACCESS_TOKEN_EXPIRE_PERIOD: int = 3600 * 24


class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = "postgresql+asyncpg://fastapi:fastapi@localhost:3303/prod"
    READER_DB_URL: str = "postgresql+asyncpg://fastapi:fastapi@localhost:3303/prod"
    ACCESS_TOKEN_EXPIRE_PERIOD: int = os.getenv("ACCESS_TOKEN_EXPIRE_PERIOD")
    REFRESH_TOKEN_EXPIRE_PERIOD: int = os.getenv("REFRESH_TOKEN_EXPIRE_PERIOD")
    TASK_CAPTURE_EXCEPTIONS: bool = False


class TestConfig(Config):
    WRITER_DB_URL: str = "sqlite+aiosqlite:///./test.db"
    READER_DB_URL: str = "sqlite+aiosqlite:///./test.db"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
        "test": TestConfig(),
    }
    return config_type[env]


config: Config = get_config()
