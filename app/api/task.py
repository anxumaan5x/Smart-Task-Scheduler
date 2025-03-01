from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def get_tasks():
    return {"tasks": ["Task 1", "Task 2"]}