from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from config.database_connector import get_db
from model.db_model import User
from model.schema import UserResponse, UserCreate, Token

from fastapi import APIRouter

from services.auth_utils import hash_password, create_access_token

router = APIRouter()

@router.post("/create/", response_model=Token)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}