from fastapi import Form    # Form is a class
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str

    @classmethod
    def student_form(cls, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
        return cls(
            username=username,
            email=email,
            password=password)
        