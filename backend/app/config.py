from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Inversiones IA"
    app_env: str = "local"
    debug: bool = True
    database_url: str = "mysql+pymysql://inv_user:inv_password@127.0.0.1:3307/inversiones_ia"
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"
    secret_key: str = "change-me-in-production"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
