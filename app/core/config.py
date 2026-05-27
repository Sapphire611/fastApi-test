import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    DEBUG: bool = False
    PROJECT_NAME: str = "FastAPI Project"
    API_V1_STR: str = "/api/v1"

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""  # service_role key for server-side operations
    SUPABASE_JWT_SECRET: str = ""

    # Password hashing (must match frontend NEXT_PUBLIC_PASSWORD_SALT)
    PASSWORD_SALT: str = "infp-cms-fixed-salt-2024"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()

logger.info(
    "Supabase target: %s",
    settings.SUPABASE_URL or "(not configured)",
)
