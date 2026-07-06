from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.stats import MonthlyStatsResponse, ByCategoryStatsResponse, MonthlyTrendResponse, TopExpensesResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
import app.services.stats as stats_service
import app.services.user as user_service

router = APIRouter(tags=["Stats"], prefix="/stats")

@router.get("/monthly", response_model=MonthlyStatsResponse)
def read_monthly_stats(month: int | None = None, year: int | None = None, db: Session = Depends(get_db)):
    return stats_service.get_monthly_stats(month=month, year=year, db=db)

@router.get("/by-category", response_model=list[ByCategoryStatsResponse])
def read_stats_by_category(db: Session = Depends(get_db)):
    return stats_service.get_stats_expenses_by_category(db=db)

@router.get("/balance")
def read_stats_balance(user_id: int | None = None, account_id: int | None = None, db: Session = Depends(get_db)):
    try:
        return stats_service.get_stats_balance(user_id=user_id, account_id=account_id, db=db)
    except user_service.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except stats_service.AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
@router.get("/top-expenses", response_model=list[TopExpensesResponse])
def read_top_expenses(limit: int = 10, offset: int = 0, user_id: int | None = None, account_id: int | None = None, db: Session = Depends(get_db)):
    try:
        return stats_service.get_top_expenses(limit=limit, offset=offset, user_id=user_id, account_id=account_id, db=db)
    except user_service.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except stats_service.AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
@router.get("/monthly-trend", response_model=list[MonthlyTrendResponse])
def read_monthly_trend(user_id: int | None = None, account_id: int | None = None, db: Session = Depends(get_db)):
    try:
        return stats_service.get_monthly_trend(user_id=user_id, account_id=account_id, db=db)
    except user_service.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except stats_service.AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    