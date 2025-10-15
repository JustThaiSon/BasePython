from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None

class LoginResponse(BaseModel):
    access_token: str
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    gender: Optional[str]
    date_of_birth: Optional[date]
    is_active: bool

    class Config:
        from_attributes = True
