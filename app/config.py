from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import make_url

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"
    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def get_sync_database_url(self) -> str:
        url = make_url(self.DATABASE_URL)
        if "+" in url.drivername:
            new_driver = url.drivername.split("+")[0]
            return str(url.set(drivername=new_driver))
        return self.DATABASE_URL

settings = Settings()
