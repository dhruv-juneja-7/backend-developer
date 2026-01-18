from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr

class ActionCreate(BaseModel):
    user_id: int 
    status: str

class ActionResponse(BaseModel):
    id: int
    status: str

