from sqlalchemy.orm import Session
from app.models.category import Category
from app.exceptions.category_exceptions import CategoryAlreadyExists, CategoryNotFound

def get_categories(db: Session):
    """Return all categories."""

    return db.query(Category).all()

def get_category_by_id(category_id: int, db: Session):
    """Return a category by its ID."""

    category = db.query(Category).where(Category.id == category_id).first()

    if not category:
        raise CategoryNotFound()
    
    return category

def get_category_by_name(category_name: str, db: Session):
    """Return a category by its name."""

    return db.query(Category).where(Category.name == category_name).first() 

def create_category(category: Category, db: Session):
    """Create a new category."""

    if get_category_by_name(category_name=category.name, db=db):
        raise CategoryAlreadyExists()

    category_db = Category(name=category.name)

    db.add(category_db)
    db.commit()
    db.refresh(category_db)

    return category_db

def update_category(category_id: int, category: Category, db: Session):
    """Update an existing category."""

    category_db = get_category_by_id(category_id=category_id, db=db)

    if category.name == category_db.name:
        return category_db

    if get_category_by_name(category_name=category.name, db=db):
        raise CategoryAlreadyExists()

    if category.name is not None:
        category_db.name = category.name

    db.commit()
    db.refresh(category_db)

    return category_db

def delete_category(category_id: int, db: Session):
    """Delete a category."""

    category = get_category_by_id(category_id=category_id, db=db)

    db.delete(category)
    db.commit()

    return
