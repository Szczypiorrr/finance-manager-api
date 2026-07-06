import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.expense import Expense
from app.models.income import Income
from app.models.account import Account
from app.models.category import Category

from datetime import datetime

from app.services.stats import (
    get_monthly_stats,
    get_stats_expenses_by_category,
    get_stats_balance,
    get_top_expenses,
    get_monthly_trend
)

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_get_monthly_stats_basic(db):
    # given
    account = Account(name="acc1", user_id=1)
    db.add(account)
    db.commit()

    test_date = datetime(2026, 1, 15)

    expense = Expense(amount=100, account_id=account.id, created_at=test_date)
    income = Income(amount=200, account_id=account.id, created_at=test_date)

    db.add_all([expense, income])
    db.commit()

    # when
    result = get_monthly_stats(db, month=1, year=2026)

    # then
    assert result["total_expenses"] == 100
    assert result["total_income"] == 200


def test_get_stats_expenses_by_category(db):
    # given
    category = Category(name="Food")
    db.add(category)
    db.commit()

    expense1 = Expense(amount=50, category_id=category.id)
    expense2 = Expense(amount=30, category_id=category.id)

    db.add_all([expense1, expense2])
    db.commit()

    # when
    result = get_stats_expenses_by_category(db)

    # then
    assert len(result) == 1
    assert result[0]["category_name"] == "Food"
    assert result[0]["total_expenses"] >= 80


def test_get_stats_balance_base(db):
    # when
    result = get_stats_balance(db)

    # then
    assert result.total_expenses == 0
    assert result.total_income == 0
    assert result.balance == 0


def test_get_top_expenses_basic(db):
    # given
    account = Account(name="acc1", user_id=1)
    category = Category(name="Food")

    db.add_all([account, category])
    db.commit()

    exp1 = Expense(amount=100, description="A", account_id=account.id, category_id=category.id)
    exp2 = Expense(amount=200, description="B", account_id=account.id, category_id=category.id)

    db.add_all([exp1, exp2])
    db.commit()

    # when
    result = get_top_expenses(None, None, db, limit=10)

    # then
    assert len(result) >= 2
    assert result[0]["amount"] >= result[1]["amount"]


def test_get_monthly_trend_basic(db):
    # given
    account = Account(name="acc1", user_id=1)
    db.add(account)
    db.commit()

    expense = Expense(amount=100, account_id=account.id)
    db.add(expense)
    db.commit()

    # when
    result = get_monthly_trend(None, None, db)

    # then
    assert isinstance(result, list)