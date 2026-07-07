from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.budget import BudgetResponse, BudgetCreate, BudgetUpdate
from sqlalchemy.orm import Session
from app.core.database import get_db
import app.services.budget as budget_service
from app.exceptions.budget_exceptions import BudgetNotFound, BudgetAlreadyExists
from app.exceptions.user_exceptions import UserNotFound
from app.exceptions.category_exceptions import CategoryNotFound
from app.exceptions.common_exceptions import InvalidAmount

router = APIRouter(tags=["Budget"], prefix="/budgets")

@router.get("/", response_model=list[BudgetResponse])
def read_budgets(limit: int = 10, offset: int = 0, user_id: int = None, category_id: int = None, db: Session = Depends(get_db)):
    return budget_service.get_budgets(db=db, user_id=user_id, category_id=category_id, limit=limit, offset=offset)

@router.get("/{budget_id}", response_model=BudgetResponse)
def read_budget(budget_id: int, db: Session = Depends(get_db)):
    try:
        return budget_service.get_budget_by_id(budget_id=budget_id, db=db)
    except BudgetNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    
@router.post("/", response_model=BudgetResponse)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    try:
        return budget_service.create_budget(budget=budget, db=db)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    except BudgetAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Budget for this user, category and period already exists")
    
@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    try:
        return budget_service.delete_budget(budget_id=budget_id, db=db)
    except BudgetNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")

    
@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(budget_id: int, budget_update: BudgetUpdate, db: Session = Depends(get_db)):
    try:
        return budget_service.update_budget(budget_id=budget_id, budget_update=budget_update, db=db)
    except BudgetNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    except InvalidAmount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount")