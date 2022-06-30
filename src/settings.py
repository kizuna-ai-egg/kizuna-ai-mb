from functools import lru_cache
from pydantic import BaseSettings


class OAuth2Settings(BaseSettings):
    client_id: str
    client_secret: str
    redirect_uri: str


@lru_cache()
def get_github() -> OAuth2Settings:
    return OAuth2Settings(
        client_id='',
        client_secret='',
        redirect_uri=''
    )
