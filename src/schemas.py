from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_lenght=10)

class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"

class ContactCreate(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_info: Optional[str] = None


class ContactResponse(ContactCreate):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"