# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # prevents bcrypt error

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
