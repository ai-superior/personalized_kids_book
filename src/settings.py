from pydantic import Field
from pydantic_settings import BaseSettings


class WebserverSettings(BaseSettings):
    host: str = ""
    port: int = 8000
    cors_origin: str = "*"
    protocol: str = ""
    static_dir: str = ""
    domain: str = ""


class MongoSettings(BaseSettings):
    mongo_client: str = ""
    db: str = ""


class HubSpotSettings(BaseSettings):
    host: str = ""
    access_token: str = ""


class Settings(BaseSettings):
    mongo: MongoSettings = Field(default_factory=MongoSettings)
    webserver: WebserverSettings = Field(default_factory=WebserverSettings)
    hubspot: HubSpotSettings = Field(default_factory=HubSpotSettings)

    debug: bool = True

    class Config:
        env_nested_delimiter = "__"
        env_file = ".env"
        extra = "ignore"


SETTINGS = Settings()
