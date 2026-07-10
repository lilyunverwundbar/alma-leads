from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8")

    app_name: str = "Alma Leads API"
    app_env: str = "local"
    database_url: str = "sqlite:///./storage/leads.db"
    public_web_url: str = "http://localhost:3000"
    internal_attorney_email: str = "attorney@example.com"
    from_email: str = "leads@example.com"
    admin_username: str = "attorney@company.com"
    admin_password: str = "change-me"
    auth_secret: str = "replace-with-a-long-random-secret"
    access_token_minutes: int = 12 * 60
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    storage_dir: Path = BASE_DIR / "storage"
    max_resume_bytes: int = 10 * 1024 * 1024

    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = True

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

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
