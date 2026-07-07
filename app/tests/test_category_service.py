import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.schemas.category import CategoryCreate
from app.services.category import create_category, get_categories, get_category_by_id, get_category_by_name, update_category, delete_category
from app.exceptions.category_exceptions import CategoryAlreadyExists, CategoryNotFound

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

def test_create_category_success(db):
    """Creates a category successfully."""

    # given
    category_data = CategoryCreate(name="Test Category")

    # when
    category = create_category(category=category_data, db=db)

    # then
    assert category.name == "Test Category"
    assert category.id is not None

def test_get_all_categories_empty_database(db):
    """Returns empty list when no categories exist."""

    # when
    categories = get_categories(db=db)

    # then
    assert categories == []

def test_get_all_categories(db):
    """Returns all existing categories."""

    # given
    category1 = create_category(category=CategoryCreate(name="Category 1"), db=db)
    category2 = create_category(category=CategoryCreate(name="Category 2"), db=db)

    # when
    categories = get_categories(db=db)

    # sortowanie żeby kolejność była pewna
    categories = sorted(categories, key=lambda c: c.id)

    # then
    assert len(categories) == 2

    assert categories[0].name == category1.name
    assert categories[1].name == category2.name

def test_get_category_by_id_success(db):
    """Returns category by ID."""

    # given
    category = create_category(category=CategoryCreate(name="Test Category"), db=db)

    # when
    retrieved_category = get_category_by_id(category_id=category.id, db=db)

    # then
    assert retrieved_category.id == category.id
    assert retrieved_category.name == category.name

def test_get_category_by_id_not_found(db):
    """Raises error when category does not exist."""

    # given
    non_existing_id = 999

    # when / then
    with pytest.raises(CategoryNotFound):
        get_category_by_id(category_id=non_existing_id, db=db)

def test_create_category_duplicate_raises_exception(db):
    """Prevents creating duplicate categories."""

    # given
    category_data = CategoryCreate(name="Duplicate Category")
    create_category(category=category_data, db=db)

    # when / then
    with pytest.raises(CategoryAlreadyExists):
        create_category(category=category_data, db=db)

def test_get_category_by_name_success(db):
    """Returns category by name."""

    # given
    category_data = CategoryCreate(name="Test Category")
    created_category = create_category(category=category_data, db=db)

    # when
    retrieved_category = get_category_by_name(category_name=created_category.name, db=db)

    # then
    assert retrieved_category.id == created_category.id
    assert retrieved_category.name == created_category.name

def test_get_category_by_name_not_found(db):
    """Returns None when category name does not exist."""

    # given
    non_existing_name = "Non Existing Category"

    # when
    retrieved_category = get_category_by_name(category_name=non_existing_name, db=db)

    # then
    assert retrieved_category is None

def test_update_category_success(db):
    """Updates category name successfully."""

    # given
    category = create_category(category=CategoryCreate(name="Old Name"), db=db)

    # when
    updated_category = update_category(category_id=category.id, category=CategoryCreate(name="New Name"), db=db)

    # then
    assert updated_category.name == "New Name"
    assert updated_category.id == category.id

def test_delete_category_success(db):
    """Deletes category successfully."""

    # given
    category = create_category(category=CategoryCreate(name="To Be Deleted"), db=db)

    # when
    delete_category(category_id=category.id, db=db)

    # then
    with pytest.raises(CategoryNotFound):
        get_category_by_id(category_id=category.id, db=db)