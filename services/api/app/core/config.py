from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NexusQuant Explosive Hunter API"
    environment: str = "production"
    database_url: str = "postgresql+asyncpg://nexusquant:nexusquant@postgres:5432/nexusquant"
    redis_url: str = "redis://redis:6379/0"
    upstox_client_id: str = ""
    upstox_client_secret: str = ""
    newsapi_key: str = ""
    finnhub_key: str = ""
    telegram_webhook_url: str = ""
    discord_webhook_url: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
