from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    db_hostname: str = Field(..., env="DATABASE_HOSTNAME")
    db_port: str = Field(..., env="DATABASE_PORT")
    db_name: str = Field(..., env="DATABASE_NAME")
    db_username: str = Field(..., env="DATABASE_USERNAME")
    db_password: str = Field(..., env="DATABASE_PASSWORD")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        orm_mode = True
        env_file = '.env'

@lru_cache
def get_settings():
    return Settings()