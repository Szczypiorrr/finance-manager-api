from models.income import Income
from schemas.income import IncomeCreate, IncomeUpdate
from sqlalchemy.orm import Session
from services.account import get_account_by_id
from datetime import datetime
from helpers.datetime import current_datetime
from helpers.validators import validate_amount
from exceptions.income_exceptions import IncomeNotFound


def get_incomes(db: Session, account_id: int | None = None, start_date: datetime | None = None, end_date: datetime | None = None, limit: int = 10, offset: int = 0):
    query = db.query(Income)

    if account_id is not None:
        query = query.where(Income.account_id == account_id)

    if start_date is not None:
        query = query.where(Income.created_at >= start_date)

    if end_date is not None:
        query = query.where(Income.created_at <= end_date)

    return query.limit(limit).offset(offset).all()

def get_income_by_id(income_id: int, db: Session):
    income = db.query(Income).where(Income.id == income_id).first()

    if not income:
        raise IncomeNotFound()
    
    return income

def create_income(income: IncomeCreate, db: Session):
    get_account_by_id(account_id=income.account_id, db=db)

    income_db = Income(
        amount=income.amount,
        source=income.source,
        created_at=current_datetime(),
        account_id=income.account_id
    )

    db.add(income_db)
    db.commit()
    db.refresh(income_db)

    return income_db

def delete_income(income_id: int, db: Session):
    income = get_income_by_id(income_id=income_id, db=db)

    db.delete(income)
    db.commit()

    return

def update_income(income_id: int, income_update: IncomeUpdate, db: Session):
    income = get_income_by_id(income_id=income_id, db=db)

    if income_update.amount is not None:
        validate_amount(income_update.amount)
        income.amount = income_update.amount

    if income_update.source is not None:
        income.source = income_update.source

    db.commit()
    db.refresh(income)

    return income