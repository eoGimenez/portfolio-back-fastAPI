from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str
    username: Optional[str]
