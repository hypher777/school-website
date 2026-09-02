import secrets
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file.

    For production, use environment variables only.
    """

    # Application
    app_name: str = "School Website"
    app_env: str = "development"
    debug: bool = False

    # Database
    database_url: str = "postgresql://localhost:5432/school_db"
    database_pool_size: int = Field(default=5, ge=1)
    database_max_overflow: int = Field(default=10, ge=0)
    database_pool_recycle: int = Field(default=1800, ge=0)

    # Security
    secret_key: str = secrets.token_urlsafe(32)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # Deployment hosts
    allowed_hosts: str = "localhost,127.0.0.1,testserver"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def allowed_hosts_list(self) -> list[str]:
        return [host.strip() for host in self.allowed_hosts.split(",") if host.strip()]

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        if self.app_env.lower() == "production":
            if self.debug:
                raise ValueError("DEBUG must be false in production")
            if len(self.secret_key) < 32 or self.secret_key == "change-me-in-production":
                raise ValueError("SECRET_KEY must be a strong production secret")
            if not self.cors_origins_list:
                raise ValueError("CORS_ORIGINS must contain an allowed origin")
        return self


settings = Settings()
