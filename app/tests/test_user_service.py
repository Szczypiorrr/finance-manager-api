import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.services.user import create_user, get_user_by_username, update_user, delete_user, get_user_by_id
from app.exceptions.user_exceptions import UserAlreadyExists, UserNotFound
from app.core.database import Base
from app.schemas.user import UserUpdate

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

def test_get_user_success(db):
    # given
    username = "testuser"
    create_user(username=username, db=db)

    # when
    user = get_user_by_username(username=username, db=db)

    # then
    assert user is not None
    assert user.username == username

def test_create_user_success(db):
    # given
    username = "testuser"

    # when
    user = create_user(username=username, db=db)

    # then
    assert user.username == username
    assert user.id is not None


def test_user_existing(db):
    # given
    username = "existinguser"

    create_user(username=username, db=db)

    # when
    user = get_user_by_username(username=username, db=db)

    # then
    assert user is not None

def test_user_not_existing(db):
    # given
    username = "nonexistinguser"
    
    # when
    user = get_user_by_username(username=username, db=db)

    # then
    assert user is None

def test_create_user_duplicate_raises_exception(db):
    # given
    username = "testuser"

    create_user(username=username, db=db)

    # when / then
    with pytest.raises(UserAlreadyExists):
        create_user(username=username, db=db)

def test_update_user_success(db):
    # given
    user = create_user(username="old_name", db=db)

    update_data = UserUpdate(username="new_name")

    # when
    updated_user = update_user(user_id=user.id, username=update_data.username, db=db)

    # then
    assert updated_user.username == "new_name"

def test_delete_user_success(db):
    # given
    user = create_user(username="to_delete", db=db)

    # when
    delete_user(user_id=user.id, db=db)

    # then
    with pytest.raises(UserNotFound):
        get_user_by_id(user_id=user.id, db=db)
