from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    app_name: str = "Inversiones IA"
    app_env: str = "local"
    debug: bool = True
    database_url: str = "mysql+pymysql://inv_user:inv_password@127.0.0.1:3306/inversiones_ia"
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"
    secret_key: str = "change-me-in-production"

    model_config = SettingsConfigDict(
        env_file=(PROJECT_DIR / ".env", BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
