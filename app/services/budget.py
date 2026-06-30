from sqlalchemy.orm import Session
from sqlalchemy import and_
from services.user import get_user_by_id
from services.category import get_category_by_id
from models.budget import Budget
from schemas.budget import BudgetCreate, BudgetUpdate
from datetime import datetime

class BudgetNotFound(Exception):
    pass

class BudgetAlreadyExists(Exception):
    pass

class InvalidAmount(Exception):
    pass

def get_budgets(db: Session, user_id: int = None, category_id: int = None, limit: int = 10, offset: int = 0):
    query = db.query(Budget)

    if user_id is not None:
        query = query.where(Budget.user_id == user_id)

    if category_id is not None:
        query = query.where(Budget.category_id == category_id)

    return query.limit(limit).offset(offset).all()

def get_budget_by_id(budget_id: int, db: Session):
    budget = db.query(Budget).where(Budget.id == budget_id).first()

    if not budget:
        raise BudgetNotFound()
    
    return budget

def get_budget_by_period(user_id: int, category_id: int, month: int, year: int, db: Session):
    return db.query(Budget).where(and_(Budget.user_id == user_id, Budget.category_id == category_id, Budget.month == month, Budget.year == year)).first()

def create_budget(budget: BudgetCreate, db: Session):
    get_user_by_id(user_id=budget.user_id, db=db)
    get_category_by_id(category_id=budget.category_id, db=db)

    if get_budget_by_period(user_id=budget.user_id, category_id=budget.category_id, month=datetime.now().month, year=datetime.now().year, db=db):
        raise BudgetAlreadyExists()

    budget_db = Budget(
        limit_amount=budget.limit_amount,
        month=datetime.now().month,
        year=datetime.now().year,
        user_id=budget.user_id,
        category_id=budget.category_id
    )

    db.add(budget_db)
    db.commit()
    db.refresh(budget_db)

    return budget_db

def delete_budget(budget_id: int, db: Session):
    budget = get_budget_by_id(budget_id=budget_id, db=db)

    db.delete(budget)
    db.commit()

    return

def update_budget(budget_id: int, budget_update: BudgetUpdate, db: Session):
    budget = get_budget_by_id(budget_id=budget_id, db=db)

    if budget_update.limit_amount <= 0:
        raise InvalidAmount()

    if budget.limit_amount == budget_update.limit_amount:
        return budget

    if budget_update.limit_amount is not None:
        budget.limit_amount = budget_update.limit_amount

    db.commit()
    db.refresh(budget)

    return budget