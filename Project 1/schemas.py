from pydantic import BaseModel, Field, EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr