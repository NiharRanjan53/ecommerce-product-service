from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from src.enums.roles import Role
from datetime import datetime
from uuid import uuid4

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role  # ADMIN | SELLER | USER
   

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type : str = "bearer"

class UserInDB(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    profile_image: Optional[str] = None

    password_hash: str
    role: Role

    is_active: bool = True
    is_verified: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    password: Optional[str] = None