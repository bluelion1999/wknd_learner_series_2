from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import CategoryDB
from schemas import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("", response_model=list[CategoryResponse])
def get_categories(db: Session=Depends(get_db)):
    db_category = db.query(CategoryDB).all()
    return db_category

@router.post("", response_model=CategoryResponse)
def post_categories(category: CategoryCreate, db: Session=Depends(get_db)):
    db_category = CategoryDB(name = category.name, description = category.description)
    try:   
        db.add(db_category)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Category name already exists")
    db.refresh(db_category)
    return db_category