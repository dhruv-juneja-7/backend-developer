from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True 


class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr

class ActionResponse(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True

