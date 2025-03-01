from fastapi import APIRouter, Depends

from services.auth_utils import get_current_user

router = APIRouter()

@router.get("/")
def get_tasks(current_user: str = Depends(get_current_user)):
    print(current_user)
    return {"tasks": ["Task 1", "Task 2"]}