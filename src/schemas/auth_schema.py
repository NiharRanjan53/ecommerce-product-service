from pydantic import BaseModel, EmailStr
from typing import Optional
from src.enums.roles import Role

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: Role  # ADMIN | SELLER | USER
    name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type : str = "bearer"