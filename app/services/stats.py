from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models.expense import Expense
from models.income import Income
from models.account import Account
from schemas.stats import BalanceBaseResponse, UserAccountBalanceResponse, UserBalanceResponse, AccountBalanceResponse
from datetime import datetime
from services.category import get_category_by_id
from services.user import get_user_by_id
from services.account import get_account_by_id, AccountNotFound


def get_monthly_stats(db: Session, month: int | None = None, year: int | None = None):

    if month is None:
        month = datetime.now().month

    if year is None:
        year = datetime.now().year

    start_of_month = datetime(year, month, 1)

    if month == 12:
        start_of_next_month = datetime(year + 1, 1, 1)
    else:
        start_of_next_month = datetime(year, month + 1, 1)

    total_expenses = db.query(func.sum(Expense.amount)).where(and_(Expense.created_at >= start_of_month, Expense.created_at < start_of_next_month)).scalar() or 0

    total_income = db.query(func.sum(Income.amount)).where(and_(Income.created_at >= start_of_month, Income.created_at < start_of_next_month)).scalar() or 0

    balance = total_income - total_expenses

    expenses_count = db.query(func.count(Expense.id)).where(and_(Expense.created_at >= start_of_month, Expense.created_at < start_of_next_month)).scalar() or 0

    income_count = db.query(func.count(Income.id)).where(and_(Income.created_at >= start_of_month, Income.created_at < start_of_next_month)).scalar() or 0

    transactions_count = expenses_count + income_count

    return {
        "total_expenses": total_expenses,
        "total_income": total_income,
        "balance": balance,
        "transactions_count": transactions_count
    }

def get_stats_expenses_by_category(db: Session):
    expenses_by_category = db.query(Expense.category_id, func.sum(Expense.amount).label("total_expenses")).group_by(Expense.category_id).all()
    
    return [{"category_name": get_category_by_id(category_id=category_id, db=db).name, "total_expenses": round(total_expenses, 2)} for category_id, total_expenses in expenses_by_category]

def get_stats_balance(db: Session, user_id: int | None = None, account_id: int | None = None):
    if user_id and account_id:
        user = get_user_by_id(user_id=user_id, db=db)
        account = get_account_by_id(account_id=account_id, db=db)

        if db.query(Account).where(and_(Account.id == account_id, Account.user_id == user_id)).first() is None:
            raise AccountNotFound()

        total_expenses = db.query(func.sum(Expense.amount)).where(and_(Expense.account_id == account_id, Expense.account.has(user_id=user_id))).scalar() or 0
        total_income = db.query(func.sum(Income.amount)).where(and_(Income.account_id == account_id, Income.account.has(user_id=user_id))).scalar() or 0

        balance = total_income - total_expenses

        return UserAccountBalanceResponse(username=user.username, account_name=account.name, total_expenses=round(total_expenses, 2), total_income=round(total_income, 2), balance=round(balance, 2))

    elif user_id:
        user = get_user_by_id(user_id=user_id, db=db)

        accounts = db.query(Account).where(Account.user_id == user_id).all()

        total_expenses = 0
        total_income = 0
        for account in accounts:
            total_expenses += db.query(func.sum(Expense.amount)).where(Expense.account_id == account.id).scalar() or 0
            total_income += db.query(func.sum(Income.amount)).where(Income.account_id == account.id).scalar() or 0

        balance = total_income - total_expenses

        return UserBalanceResponse(username=user.username, total_expenses=round(total_expenses, 2), total_income=round(total_income, 2), balance=round(balance, 2))
    
    elif account_id:
        account = get_account_by_id(account_id=account_id, db=db)

        total_expenses = db.query(func.sum(Expense.amount)).where(Expense.account_id == account_id).scalar() or 0
        total_income = db.query(func.sum(Income.amount)).where(Income.account_id == account_id).scalar() or 0

        balance = total_income - total_expenses

        return AccountBalanceResponse(account_name=account.name, total_expenses=round(total_expenses, 2), total_income=round(total_income, 2), balance=round(balance, 2))

    else:
        total_expenses = db.query(func.sum(Expense.amount)).scalar() or 0
        total_income = db.query(func.sum(Income.amount)).scalar() or 0

        balance = total_income - total_expenses

        return BalanceBaseResponse(total_expenses=round(total_expenses, 2), total_income=round(total_income, 2), balance=round(balance, 2))


def get_top_expenses(user_id: int | None, account_id: int | None, db: Session, limit: int = 10, offset: int = 0):
    if user_id and account_id:
        get_user_by_id(user_id=user_id, db=db)
        get_account_by_id(account_id=account_id, db=db)

        if db.query(Account).where(and_(Account.id == account_id, Account.user_id == user_id)).first() is None:
            raise AccountNotFound()

        top_expenses = db.query(Expense).where(and_(Expense.account_id == account_id, Expense.account.has(user_id=user_id))).order_by(Expense.amount.desc()).limit(limit).offset(offset).all()

        return [{"amount": expense.amount, "description": expense.description, "created_at": expense.created_at, "account_name": expense.account.name, "category_name": expense.category.name} for expense in top_expenses]
    
    elif user_id:
        get_user_by_id(user_id=user_id, db=db)

        accounts = db.query(Account.id).where(Account.user_id == user_id).all()
        account_ids = [a.id for a in accounts]

        top_expenses = (db.query(Expense).where(Expense.account_id.in_(account_ids)).order_by(Expense.amount.desc()).limit(limit).offset(offset).all())

        return [{"amount": expense.amount,"description": expense.description,"created_at": expense.created_at,"account_name": expense.account.name,"category_name": expense.category.name,}for expense in top_expenses]
    
    elif account_id:
        get_account_by_id(account_id=account_id, db=db)

        top_expenses = db.query(Expense).where(Expense.account_id == account_id).order_by(Expense.amount.desc()).limit(limit).offset(offset).all()

        return [{"amount": expense.amount, "description": expense.description, "created_at": expense.created_at, "account_name": expense.account.name, "category_name": expense.category.name} for expense in top_expenses]
    
    else:
        top_expenses = db.query(Expense).order_by(Expense.amount.desc()).limit(limit).offset(offset).all()

        return [{"amount": expense.amount, "description": expense.description, "created_at": expense.created_at, "account_name": expense.account.name, "category_name": expense.category.name} for expense in top_expenses]


def get_monthly_trend(user_id: int | None, account_id: int | None, db: Session):
    if user_id and account_id:
        get_user_by_id(user_id=user_id, db=db)
        get_account_by_id(account_id=account_id, db=db)

        if db.query(Account).where(and_(Account.id == account_id, Account.user_id == user_id)).first() is None:
            raise AccountNotFound()

        monthly_trend = db.query(func.strftime("%Y-%m", Expense.created_at).label("month"), func.sum(Expense.amount).label("total_expenses")).where(and_(Expense.account_id == account_id, Expense.account.has(user_id=user_id))).group_by("month").order_by("month").all()

        return [{"month": month, "total_expenses": round(total_expenses, 2)} for month, total_expenses in monthly_trend]
    
    elif user_id:
        get_user_by_id(user_id=user_id, db=db)

        account_ids = [a.id for a in db.query(Account.id).where(Account.user_id == user_id).all()]

        monthly_trend = db.query(func.strftime("%Y-%m", Expense.created_at).label("month"),func.sum(Expense.amount).label("total_expenses")).where(Expense.account_id.in_(account_ids)).group_by("month").order_by("month").all()

        return [{"month": month, "total_expenses": round(total_expenses, 2)}for month, total_expenses in monthly_trend]
    
    elif account_id:
        get_account_by_id(account_id=account_id, db=db)

        monthly_trend = db.query(func.strftime("%Y-%m", Expense.created_at).label("month"), func.sum(Expense.amount).label("total_expenses")).where(Expense.account_id == account_id).group_by("month").order_by("month").all()

        return [{"month": month, "total_expenses": round(total_expenses, 2)} for month, total_expenses in monthly_trend]
    
    else:
        monthly_trend = db.query(func.strftime("%Y-%m", Expense.created_at).label("month"), func.sum(Expense.amount).label("total_expenses")).group_by("month").order_by("month").all()

        return [{"month": month, "total_expenses": round(total_expenses, 2)} for month, total_expenses in monthly_trend]
    
