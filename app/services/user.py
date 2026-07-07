from app.models.user import User
from sqlalchemy.orm import Session
from app.exceptions.user_exceptions import UserNotFound, UserAlreadyExists

def get_users(db: Session):
    """Returns all users."""

    return db.query(User).all()


def get_user_by_id(user_id: int, db: Session):
    """Returns a user by ID."""

    user = db.query(User).where(User.id == user_id).first()
    
    if not user:
        raise UserNotFound()

    return user


def get_user_by_username(username: str, db: Session):
    """Returns a user by username."""

    return db.query(User).where(User.username == username).first()

def create_user(username: str, db: Session):
    """Creates a new user."""

    if get_user_by_username(username=username, db=db):
        raise UserAlreadyExists()
    
    user = User(username=username)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
    
def delete_user(user_id: int, db: Session):
    """Deletes a user by ID."""

    user = get_user_by_id(user_id=user_id, db=db)

    db.delete(user)
    db.commit()
    return

def update_user(user_id: int, username: str, db: Session):
    """Updates user data."""

    user = get_user_by_id(user_id=user_id, db=db)

    if user.username == username:
        return user

    if get_user_by_username(username=username, db=db):
        raise UserAlreadyExists()

    if username:
        user.username = username

    db.commit()
    db.refresh(user)

    return user