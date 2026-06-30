from sqlalchemy.orm import Session
from models.expense import Expense
from schemas.expense import ExpenseCreate, ExpenseUpdate
from services.user import get_user_by_id
from services.account import get_account_by_id
from services.category import get_category_by_id
from datetime import datetime

class ExpenseNotFound(Exception):
    pass

def get_expenses(db: Session, user_id: int | None = None, category_id: int | None = None, account_id: int | None = None, start_date: datetime | None = None, end_date: datetime | None = None, limit: int = 10, offset: int = 0):
    query = db.query(Expense)


    if user_id is not None:
        query = query.where(Expense.user_id == user_id)

    if category_id is not None:
        query = query.where(Expense.category_id == category_id)

    if account_id is not None:
        query = query.where(Expense.account_id == account_id)

    if start_date is not None:
        query = query.where(Expense.created_at >= start_date)

    if end_date is not None:
        query = query.where(Expense.created_at <= end_date)

    query = query.limit(limit).offset(offset)

    return query.all()

def get_expense_by_id(expense_id: int, db: Session):
    expense = db.query(Expense).where(Expense.id == expense_id).first()

    if not expense:
        raise ExpenseNotFound()
    
    return expense

def create_expense(expense: ExpenseCreate, db: Session):
    get_user_by_id(user_id=expense.user_id, db=db)

    get_account_by_id(account_id=expense.account_id, db=db)

    expense_db = Expense(
        amount=expense.amount,
        description=expense.description,
        created_at=datetime.now(),
        user_id=expense.user_id,
        account_id=expense.account_id,
        category_id=expense.category_id
    )

    db.add(expense_db)
    db.commit()
    db.refresh(expense_db)

    return expense_db

def delete_expense(expense_id: int, db: Session):
    expense = get_expense_by_id(expense_id=expense_id, db=db)

    db.delete(expense)
    db.commit()

    return

def update_expense(expense_id: int, expense_update: ExpenseUpdate, db: Session):
    expense = get_expense_by_id(expense_id=expense_id, db=db)

    if expense_update.amount is not None:
        expense.amount = expense_update.amount

    if expense_update.description is not None:
        expense.description = expense_update.description

    if expense_update.category_id is not None:
        get_category_by_id(category_id=expense_update.category_id, db=db)
        expense.category_id = expense_update.category_id
        
    if expense_update.account_id is not None:
        get_account_by_id(account_id=expense_update.account_id, db=db)
        expense.account_id = expense_update.account_id

    db.commit()
    db.refresh(expense)

    return expense