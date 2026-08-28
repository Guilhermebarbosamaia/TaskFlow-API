from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from schemas.task import Task

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"

class User(BaseModel):
    id: int
    name: str
    email: EmailStr 
    role: str

    model_config = ConfigDict(from_attributes=True)