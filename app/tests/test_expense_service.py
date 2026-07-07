import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.services.expense import create_expense, get_expenses, update_expense, delete_expense, get_expense_by_id
from app.exceptions.expense_exceptions import ExpenseNotFound

from app.schemas.account import AccountCreate
from app.services.account import create_account

from app.schemas.category import CategoryCreate
from app.services.category import create_category

from app.services.user import create_user

from app.core.database import Base

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db():
    """Creates a test database session."""

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    yield session

    session.close()

    Base.metadata.drop_all(bind=engine)

def test_create_expense_success(db):
    """Creates an expense successfully."""

    # given
    user = create_user(username="testuser1", db=db)
    category = create_category(category=CategoryCreate(name="category1"), db=db)
    account = create_account(account=AccountCreate(name="account1", user_id=user.id), db=db)

    expense_data = ExpenseCreate(
        description="expense",
        amount=100.0,
        category_id=category.id,
        account_id=account.id,
    )

    # when
    expense = create_expense(expense=expense_data, db=db)

    # then
    assert expense.description == expense_data.description
    assert expense.amount == expense_data.amount
    assert expense.category_id == expense_data.category_id
    assert expense.account_id == expense_data.account_id
    assert expense.id is not None

def test_get_all_expenses_empty_database(db):
    """Returns empty list when no expenses exist."""

    # when
    expenses = get_expenses(db)

    # then
    assert len(expenses) == 0

def test_get_all_expenses(db):
    """Returns all existing expenses."""

    # given
    user1 = create_user(username="testuser1", db=db)
    category1 = create_category(category=CategoryCreate(name="category1"), db=db)
    account1 = create_account(account=AccountCreate(name="account1", user_id=user1.id), db=db)

    user2 = create_user(username="testuser2", db=db)
    category2 = create_category(category=CategoryCreate(name="category2"), db=db)
    account2 = create_account(account=AccountCreate(name="account2", user_id=user2.id), db=db)

    amount1 = 50.0
    description1 = "expense1"
    category_id1 = category1.id
    account_id1 = account1.id

    amount2 = 75.0
    description2 = "expense2"
    category_id2 = category2.id
    account_id2 = account2.id

    expense_data1 = ExpenseCreate(
        description=description1,
        amount=amount1,
        category_id=category_id1,
        account_id=account_id1
    )

    expense_data2 = ExpenseCreate(
        description=description2,
        amount=amount2,
        category_id=category_id2,
        account_id=account_id2
    )

    create_expense(expense=expense_data1, db=db)
    create_expense(expense=expense_data2, db=db)

    # when
    expenses = get_expenses(db=db)

    # then
    assert len(expenses) == 2

    assert expenses[0].description == expense_data1.description
    assert expenses[0].amount == expense_data1.amount
    assert expenses[0].category_id == expense_data1.category_id
    assert expenses[0].account_id == expense_data1.account_id

    assert expenses[1].description == expense_data2.description
    assert expenses[1].amount == expense_data2.amount
    assert expenses[1].category_id == expense_data2.category_id
    assert expenses[1].account_id == expense_data2.account_id



def test_filter_by_category(db):
    """Filters expenses by category."""

    # given
    user1 = create_user(username="testuser1", db=db)
    category1 = create_category(category=CategoryCreate(name="category1"), db=db)
    account1 = create_account(account=AccountCreate(name="account1", user_id=user1.id), db=db)

    user2 = create_user(username="testuser2", db=db)
    category2 = create_category(category=CategoryCreate(name="category2"), db=db)
    account2 = create_account(account=AccountCreate(name="account2", user_id=user2.id), db=db)

    category_id1 = category1.id
    category_id2 = category2.id

    expense_data1 = ExpenseCreate(
        description="expense1",
        amount=50.0,
        category_id=category_id1,
        account_id=account1.id
    )
    expense_data2 = ExpenseCreate(
        description="expense2",
        amount=75.0,
        category_id=category_id2,
        account_id=account2.id
    )
    expense_data3 = ExpenseCreate(
        description="expense3",
        amount=100.0,
        category_id=category_id1,
        account_id=account1.id
    )

    create_expense(expense=expense_data1, db=db)
    create_expense(expense=expense_data2, db=db)
    create_expense(expense=expense_data3, db=db)

    # when
    expenses_category1 = get_expenses(db=db, category_id=category_id1)
    expenses_category2 = get_expenses(db=db, category_id=category_id2)

    # then
    assert len(expenses_category1) == 2
    assert all(expense.category_id == category_id1 for expense in expenses_category1)

    assert len(expenses_category2) == 1
    assert all(expense.category_id == category_id2 for expense in expenses_category2)

def test_update_expense_success(db):
    """Updates expense data successfully."""

    # given
    user = create_user(username="testuser1", db=db)
    category = create_category(category=CategoryCreate(name="category1"), db=db)
    account = create_account(account=AccountCreate(name="account1", user_id=user.id), db=db)

    expense = create_expense(
        expense=ExpenseCreate(
            amount=100.0,
            description="old",
            category_id=category.id,
            account_id=account.id
        ),
        db=db
    )

    update_data = ExpenseUpdate(
        amount=200.0,
        description="new"
    )

    # when
    updated = update_expense(expense_id=expense.id, expense_update=update_data, db=db)

    # then
    assert updated.description == "new"
    assert updated.amount == 200.0

def test_delete_expense_success(db):
    """Deletes expense successfully."""

    # given
    user = create_user(username="testuser1", db=db)
    category = create_category(category=CategoryCreate(name="category1"), db=db)
    account = create_account(account=AccountCreate(name="account1", user_id=user.id), db=db)

    expense = create_expense(
        expense=ExpenseCreate(
            description="to_delete",
            amount=50.0,
            category_id=category.id,
            account_id=account.id
        ),
        db=db
    )

    # when
    delete_expense(expense_id=expense.id, db=db)

    # then
    with pytest.raises(ExpenseNotFound):
        get_expense_by_id(expense_id=expense.id, db=db)


def test_get_expense_not_found(db):
    """Raises error when expense does not exist."""

    # when / then
    with pytest.raises(ExpenseNotFound):
        get_expense_by_id(expense_id=9999, db=db)