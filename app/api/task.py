from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database_connector import get_db
from model.db_model import User, Task
from model.schema import TaskCreate, TaskResponse, UserResponse, TaskList
from services.auth_utils import get_current_user
from services.gemini_utils import get_task_deadline_and_priority
from services.task_utils import get_incomplete_tasks

router = APIRouter()

@router.get("/", response_model = UserResponse)
def get_tasks(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    return user

@router.post("/create", response_model = TaskResponse)
def create_task(task: TaskCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = get_incomplete_tasks(current_user, db)
    task_details = get_task_deadline_and_priority(task.title, tasks)
    new_task = Task(title = task.title, deadline = task_details.deadline, priority = task_details.priority)
    user = db.query(User).filter(User.username == current_user).first()
    new_task.user = user
    db.add(new_task)
    db.commit()
    return new_task

@router.get("/get_incomplete_tasks", response_model = TaskList)
def get_existing_incomplete_tasks(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = get_incomplete_tasks(current_user, db)
    return tasks

@router.patch("/complete_task/{task_id}", response_model = TaskResponse)
def complete_task(task_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    task = db.query(Task).filter(Task.id == task_id, Task.user == user).first()
    if task:
        task.completed = True
    db.commit()
    return task

