from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserResponse, UserCreate, UserUpdate
from sqlalchemy.orm import Session
from core.database import get_db
import services.user as user_service

router = APIRouter(tags=["Users"])

@router.get("/users/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return user_service.get_users(db=db)

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return user_service.get_user_by_id(user_id=user_id, db=db)
    except user_service.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(username=user.username, db=db)
    except user_service.UserAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this username already exists")

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return user_service.delete_user(user_id=user_id, db=db)
    except user_service.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        return user_service.update_user(user_id=user_id, new_username=user.new_username, db=db)
    except user_service.UserAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this username already exists")
    except user_service.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")