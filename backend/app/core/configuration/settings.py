from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "School Website"
    app_env: str = "development"
    debug: bool = True
    database_url: str = "postgresql+psycopg://school_user:school_password@localhost:5432/school_db"
    secret_key: str = "change-me-in-production"
    allowed_hosts: str = "localhost,127.0.0.1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
