from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.income import IncomeResponse, IncomeCreate, IncomeUpdate
from sqlalchemy.orm import Session
from app.core.database import get_db
import app.services.income as income_service
from datetime import datetime
from app.exceptions.income_exceptions import IncomeNotFound
from app.exceptions.account_exceptions import AccountNotFound
from app.exceptions.common_exceptions import InvalidAmount


router = APIRouter(tags=["Incomes"], prefix="/incomes")

@router.get("/", response_model=list[IncomeResponse])
def read_incomes(limit: int = 10, offset: int = 0, account_id: int | None = None, start_date: datetime | None = None, end_date: datetime | None = None, db: Session = Depends(get_db)):
    """Return a list of incomes."""

    return income_service.get_incomes(db=db, account_id=account_id, start_date=start_date, end_date=end_date, limit=limit, offset=offset)

@router.get("/{income_id}", response_model=IncomeResponse)
def read_income(income_id: int, db: Session = Depends(get_db)):
    """Return an income by its ID."""

    try:
        return income_service.get_income_by_id(income_id=income_id, db=db)
    except IncomeNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    
@router.post("/", response_model=IncomeResponse)
def create_income(income: IncomeCreate, db: Session = Depends(get_db)):
    """Create a new income."""

    try:
        return income_service.create_income(income=income, db=db)
    except AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income(income_id: int, db: Session = Depends(get_db)):
    """Delete an income."""

    try:
        return income_service.delete_income(income_id=income_id, db=db)
    except IncomeNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    
@router.put("/{income_id}", response_model=IncomeResponse)
def update_income(income_id: int, income_update: IncomeUpdate, db: Session = Depends(get_db)):
    """Update an existing income."""

    try:
        return income_service.update_income(income_id=income_id, income_update=income_update, db=db)
    except IncomeNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    except InvalidAmount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount")