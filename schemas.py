from fastapi import Form    # Form is a class
from pydantic import BaseModel
from typing import Optional


class NewUser(BaseModel):
    username: str
    email: str
    password: str

    @classmethod
    def register_form(cls, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
        return cls(
            username=username,
            email=email,
            password=password)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    username: str