from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate
from sqlalchemy.orm import Session
from app.core.database import get_db
import app.services.category as category_service
from app.exceptions.category_exceptions import CategoryNotFound, CategoryAlreadyExists

router = APIRouter(tags=["Categories"], prefix="/categories")

@router.get("/", response_model=list[CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    """Return all categories."""

    return category_service.get_categories(db=db)

@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Return a category by its ID."""

    try:
        return category_service.get_category_by_id(category_id=category_id, db=db)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category."""

    try:
        return category_service.create_category(category=category, db=db)
    except CategoryAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category with this name already exists")
    
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category."""

    try:
        return category_service.delete_category(category_id=category_id, db=db)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    """Update an existing category."""

    try:
        return category_service.update_category(category_id=category_id, category=category, db=db)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")