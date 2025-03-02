

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str


class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    category: str
    priority: Optional[int] = None
    created_at: datetime
    completed: bool
    user_id: int
    deadline: datetime
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str = None
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    username: str
    email: str = None
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskDeadLinePriority(BaseModel):
    deadline: datetime | None
    priority: int

class TaskList(BaseModel):
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True