from functools import lru_cache
from pydantic import BaseSettings, Field

# Class to setup Environment Variables
class Settings(BaseSettings):
    db_hostname: str = Field(..., env="DATABASE_HOSTNAME")
    db_port: str = Field(..., env="DATABASE_PORT")
    db_name: str = Field(..., env="DATABASE_NAME")
    db_username: str = Field(..., env="DATABASE_USERNAME")
    db_password: str = Field(..., env="DATABASE_PASSWORD")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    response_format: str = Field(..., env="RESPONSE_FORMAT")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")
    

    class Config:
        orm_mode = True
        env_file = '.env'

#lru cache is used to cache the instance of the settings class, make settings instance a little faster
@lru_cache
def get_settings():
    return Settings()