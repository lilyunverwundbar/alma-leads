from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8")

    app_name: str = "Alma Leads API"
    app_env: str = "local"
    database_url: str = "sqlite:///./storage/leads.db"
    public_web_url: str = "http://127.0.0.1:3000"
    internal_attorney_email: str = "attorney@example.com"
    from_email: str = "leads@example.com"
    admin_username: str = "attorney@company.com"
    admin_password: str = "change-me"
    auth_secret: str = "replace-with-a-long-random-secret"
    access_token_minutes: int = 12 * 60
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    storage_dir: Path = BASE_DIR / "storage"
    max_resume_bytes: int = 10 * 1024 * 1024

    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = True
    smtp_use_ssl: bool = False

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def resume_dir(self) -> Path:
        return self.storage_dir / "resumes"

    @property
    def outbox_dir(self) -> Path:
        return self.storage_dir / "outbox"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.resume_dir.mkdir(parents=True, exist_ok=True)
    settings.outbox_dir.mkdir(parents=True, exist_ok=True)
    return settings
