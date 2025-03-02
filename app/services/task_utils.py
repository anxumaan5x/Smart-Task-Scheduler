import datetime
import heapq

from fastapi import Depends
from sqlalchemy.orm import Session

from config.database_connector import get_db
from model.db_model import Task, User
from model.schema import TaskResponse, TaskList
from services.auth_utils import get_current_user

class TaskScheduler:
    def __init__(self):
        self.task_heap = []

    def add_task(self, task: TaskResponse):
        priority_value = task.priority if task.priority else 3
        deadline = task.deadline or datetime.datetime.max
        heapq.heappush(self.task_heap, (priority_value, deadline, task.created_at, task.id, task))\

    def get_all_incomplete_tasks(self) -> TaskList:
        tasks = [heapq.heappop(self.task_heap)[4] for _ in range(len(self.task_heap))]
        task_responses = [TaskResponse.model_validate(task) for task in tasks]
        return TaskList(tasks=task_responses)


def get_incomplete_tasks(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> TaskList:
    user = db.query(User).filter(User.username == current_user).first()
    tasks = db.query(Task).filter(Task.completed == False, Task.user == user).all()
    scheduler = TaskScheduler()
    for task in tasks:
        scheduler.add_task(task)
    return scheduler.get_all_incomplete_tasks()