from fastapi import APIRouter, Depends, HTTPException, status
from schemas.goal import GoalResponse, GoalCreate, GoalUpdate
from sqlalchemy.orm import Session
from core.database import get_db
import services.goal as goal_service
import services.user as user_service

router = APIRouter(tags=["Goal"], prefix="/goals")

@router.get("/", response_model=list[GoalResponse])
def read_goals(limit: int = 10, offset: int = 0, user_id: int = None, db: Session = Depends(get_db)):
    return goal_service.get_goals(db=db, user_id=user_id, limit=limit, offset=offset)

@router.get("/{goal_id}", response_model=GoalResponse)
def read_goal(goal_id: int, db: Session = Depends(get_db)):
    try:
        return goal_service.get_goal_by_id(goal_id=goal_id, db=db)
    except goal_service.GoalNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    
@router.post("/", response_model=GoalResponse)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    try:
        return goal_service.create_goal(goal=goal, db=db)
    except user_service.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except goal_service.InvalidAmount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount")
    except goal_service.GoalAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Goal with this name already exists")
    
@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    try:
        return goal_service.delete_goal(goal_id=goal_id, db=db)
    except goal_service.GoalNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    
@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: int, goal_update: GoalUpdate, db: Session = Depends(get_db)):
    try:
        return goal_service.update_goal(goal_id=goal_id, goal_update=goal_update, db=db)
    except goal_service.GoalNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    except goal_service.InvalidAmount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount")
    
@router.post("/{goal_id}/deposit", response_model=GoalResponse)
def deposit_to_goal(goal_id: int, user_id: int, amount: int, db: Session = Depends(get_db)):
    try:
        return goal_service.deposit_to_goal(goal_id=goal_id, user_id=user_id, amount=amount, db=db)
    except goal_service.GoalNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    except goal_service.InvalidAmount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount")
    except goal_service.GoalTargetAmountExceeded:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Deposit exceeds target amount")