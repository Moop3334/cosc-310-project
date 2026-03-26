from pydantic import BaseModel
from app.schema.user import User

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
