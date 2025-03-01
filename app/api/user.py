from fastapi import Depends
from sqlalchemy.orm import Session

from config.database_connector import get_db
from model.db_model import User
from model.schema import UserResponse, UserCreate

from fastapi import APIRouter
router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user