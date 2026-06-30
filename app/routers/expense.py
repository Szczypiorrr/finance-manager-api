from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas.expense import ExpenseResponse, ExpenseCreate, ExpenseUpdate
from sqlalchemy.orm import Session
from core.database import get_db
import services.expense as expense_service
import services.user as user_service
import services.account as account_service
import services.category as category_service
from datetime import datetime

router = APIRouter(tags=["Expenses"], prefix="/expenses")

@router.get("/", response_model=list[ExpenseResponse])
def read_expenses(offset: int = 0, limit: int = Query(10, le=100), account_id: int | None = None, category_id: int | None = None, start_date: datetime | None = None, end_date: datetime | None = None, db: Session = Depends(get_db)):
    return expense_service.get_expenses(limit=limit, offset=offset, account_id=account_id, category_id=category_id, start_date=start_date, end_date=end_date, db=db)

@router.get("/{expense_id}", response_model=ExpenseResponse)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    try:
        return expense_service.get_expense_by_id(expense_id=expense_id, db=db)
    except expense_service.ExpenseNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    
@router.post("/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    try:
        return expense_service.create_expense(expense=expense, db=db)
    except user_service.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except account_service.AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except category_service.CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    try:
        return expense_service.delete_expense(expense_id=expense_id, db=db)
    except expense_service.ExpenseNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    
@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense_update: ExpenseUpdate, db: Session = Depends(get_db)):
    try:
        return expense_service.update_expense(expense_id=expense_id, expense_update=expense_update, db=db)
    except expense_service.ExpenseNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    except user_service.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except category_service.CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    except account_service.AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
