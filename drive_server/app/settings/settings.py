import os
from pydantic import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    rabbit_dsn: str = os.getenv('RABBITMQ_DSN', '')
    DSN_MINIO: str = os.getenv('DSN_MINIO', '')
    MINIO_ACCESS_KEY: str = os.getenv('MINIO_ACCESS_KEY', '')
    MINIO_SECRET_KEY: str = os.getenv('MINIO_SECRET_KEY', '')
    TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_TOKEN', '')
    POSTGRES_DB:str = os.getenv("POSTGRES_DB")
    POSTGRES_USER:str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD:str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST:str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT:str = os.getenv('POSTGRES_PORT')
    POSTGRES_DSN:str = os.getenv('POSTGRES_DSN')
    POSTGRES_DSN_sqlAlchemy: str = os.getenv('POSTGRES_DSN_sqlAlchemy')
    DSN_REDIS:str = os.getenv('DSN_REDIS')


    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
