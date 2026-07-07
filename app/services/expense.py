from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.services.account import get_account_by_id
from app.services.category import get_category_by_id
from datetime import datetime
from app.helpers.datetime import current_datetime
from app.helpers.validators import validate_amount
from app.exceptions.expense_exceptions import ExpenseNotFound

def get_expenses(db: Session, account_id: int | None = None, category_id: int | None = None, start_date: datetime | None = None, end_date: datetime | None = None, limit: int = 10, offset: int = 0):
    """Return a list of expenses."""
    
    query = db.query(Expense)

    if account_id is not None:
        query = query.where(Expense.account_id == account_id)

    if category_id is not None:
        query = query.where(Expense.category_id == category_id)

    if start_date is not None:
        query = query.where(Expense.created_at >= start_date)

    if end_date is not None:
        query = query.where(Expense.created_at <= end_date)

    query = query.limit(limit).offset(offset)

    return query.all()

def get_expense_by_id(expense_id: int, db: Session):
    """Return an expense by its ID."""

    expense = db.query(Expense).where(Expense.id == expense_id).first()

    if not expense:
        raise ExpenseNotFound()
    
    return expense

def create_expense(expense: ExpenseCreate, db: Session):
    """Create a new expense."""

    get_account_by_id(account_id=expense.account_id, db=db)

    expense_db = Expense(
        amount=expense.amount,
        description=expense.description,
        created_at=current_datetime(),
        account_id=expense.account_id,
        category_id=expense.category_id
    )

    db.add(expense_db)
    db.commit()
    db.refresh(expense_db)

    return expense_db

def delete_expense(expense_id: int, db: Session):
    """Delete an expense."""

    expense = get_expense_by_id(expense_id=expense_id, db=db)

    db.delete(expense)
    db.commit()

    return

def update_expense(expense_id: int, expense_update: ExpenseUpdate, db: Session):
    """Update an existing expense."""

    expense = get_expense_by_id(expense_id=expense_id, db=db)

    if expense_update.amount is not None:
        validate_amount(expense_update.amount)
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