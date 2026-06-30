from fastapi import APIRouter, Depends, HTTPException, status
from schemas.income import IncomeResponse, IncomeCreate, IncomeUpdate
from sqlalchemy.orm import Session
from core.database import get_db
import services.income as income_service
import services.account as account_service
from datetime import datetime

router = APIRouter(tags=["Incomes"], prefix="/incomes")

@router.get("/", response_model=list[IncomeResponse])
def read_incomes(limit: int = 10, offset: int = 0, account_id: int | None = None, start_date: datetime | None = None, end_date: datetime | None = None, db: Session = Depends(get_db)):
    return income_service.get_incomes(db=db, account_id=account_id, start_date=start_date, end_date=end_date, limit=limit, offset=offset)

@router.get("/{income_id}", response_model=IncomeResponse)
def read_income(income_id: int, db: Session = Depends(get_db)):
    try:
        return income_service.get_income_by_id(income_id=income_id, db=db)
    except income_service.IncomeNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    
@router.post("/", response_model=IncomeResponse)
def create_income(income: IncomeCreate, db: Session = Depends(get_db)):
    try:
        return income_service.create_income(income=income, db=db)
    except account_service.AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income(income_id: int, db: Session = Depends(get_db)):
    try:
        return income_service.delete_income(income_id=income_id, db=db)
    except income_service.IncomeNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    
@router.put("/{income_id}", response_model=IncomeResponse)
def update_income(income_id: int, income_update: IncomeUpdate, db: Session = Depends(get_db)):
    try:
        return income_service.update_income(income_id=income_id, income_update=income_update, db=db)
    except income_service.IncomeNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    except income_service.InvalidAmount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount")