from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
USER_HOME = Path.home()
APP_DATA_DIR = USER_HOME / ".askdb"
APP_DATA_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "AskDB API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Memory DB path for chatbot
    memory_db_path: str = str(APP_DATA_DIR / "checkpoints.sqlite")

    # API Keys
    GOOGLE_API_KEY: str
    TAVILY_API_KEY: str

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 24  # 1 day

    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    all_cors_origins: list[str] = ["http://localhost:3000"]

    # Database
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{APP_DATA_DIR}/askdb.db"

    # First superuser
    FIRST_SUPERUSER: str = "admin@askdb.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin1234"

    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_ignore_empty=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
