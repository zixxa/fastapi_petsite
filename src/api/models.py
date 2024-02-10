import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class OrmModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(OrmModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: str
    is_active: bool


class DeleteUserResponse(BaseModel):
    user_id: uuid.UUID


class UserCreate(BaseModel):
    name: str
    surname: str
    email: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value
