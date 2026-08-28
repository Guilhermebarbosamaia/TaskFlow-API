from typing import Optional
from pydantic import BaseModel, ConfigDict


# User only needs to send title and description!
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    user_id: int

    model_config = ConfigDict(from_attributes=True)