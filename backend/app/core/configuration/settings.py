from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file.

    For production, use environment variables only.
    """

    # Application
    app_name: str = "School Website"
    app_env: str = "development"
    debug: bool = True

    # Database
    database_url: str = "postgresql://localhost:5432/school_db"

    # Security
    secret_key: str = "change-me-in-production"

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # Deployment hosts
    allowed_hosts: str = "localhost,127.0.0.1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
