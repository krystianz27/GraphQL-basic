# SECRET_KEY = "jwt-secret-key"
# ALGORITHM = "HS256"
# TOKEN_EXPIRATION = 15
# DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/mydb"

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    token_expiration: int
    db_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
