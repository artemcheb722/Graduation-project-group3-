from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DEBUG: bool = False



@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()