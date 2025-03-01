from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TaskBase(BaseModel):
    name: str
    priority: int

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    category: str
    created_at: datetime
    completed: bool
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str = None
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
