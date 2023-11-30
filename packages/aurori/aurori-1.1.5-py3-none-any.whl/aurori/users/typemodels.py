from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    id: int
    admin: bool


class TokenData(BaseModel):
    username: str | None = None
