import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_NAME: str = Field("auth_service", env="PROJECT_NAME")
    DB_USER: str = Field(env="DB_USER")
    DB_NAME: str = Field(env="DB_NAME")
    DB_HOST: str = Field(env="DB_HOST")
    DB_PORT: str = Field(env="DB_PORT")
    DB_PASSWORD: str = Field(env="DB_PASSWORD")
    REDIS_HOST: str = Field("127.0.0.1", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    EXPIRE: int = 5 * 60

    class Config:
        env_file = '.env'


settings = Settings()
