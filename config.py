import os

from pydantic import BaseSettings, SecretStr


class BotConfig(BaseSettings):
    bot_token: SecretStr
    aviasales_api_token: SecretStr
    db_host: str
    db_port: int
    db_user: str
    db_pass: SecretStr
    db_name: str
    ticket_price_checker_settings: str

    class Config:
        env_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
        env_file_encoding = "utf-8"


config = BotConfig()
config.ticket_price_checker_settings = os.path.expanduser(
    config.ticket_price_checker_settings
)
