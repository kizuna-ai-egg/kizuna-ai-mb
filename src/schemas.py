from pydantic import BaseModel


class Token(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str


class UserIn(BaseModel):
    id: str
    nick_name: str
    avatar_url: str
    type: str
