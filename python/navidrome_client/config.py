from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class NavidromeConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="NAVIDROME_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    url: str
    external_url: str | None = None
    user: str
    password: str

    # Constants
    api_version: str = "1.16.1"
    client_name: str = "python-navidrome-client"


@lru_cache(maxsize=1)
def get_settings() -> NavidromeConfig:
    """Cached factory — returns the same instance for the whole app lifetime."""
    return NavidromeConfig()

