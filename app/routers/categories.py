from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import PaginationParams
from app.models import CategoryDB
from app.schemas import CategoryCreate, CategoryResponse, DeleteResponse

router = APIRouter(prefix="/categories", tags=["categories"])


def get_category_or_404(
    category_id: int, db: Session = Depends(get_db)
) -> CategoryDB:
    db_category = db.get(CategoryDB, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("", response_model=list[CategoryResponse])
def list_categories(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
):
    db_categories = db.execute(
        select(CategoryDB)
        .order_by(CategoryDB.id)
        .offset(pagination.skip)
        .limit(pagination.limit)
    ).scalars().all()
    return db_categories


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(db_category: CategoryDB = Depends(get_category_or_404)):
    return db_category


@router.post("", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = CategoryDB(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category: CategoryCreate,
    db_category: CategoryDB = Depends(get_category_or_404),
    db: Session = Depends(get_db),
):
    db_category.name = category.name
    db_category.description = category.description

    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{category_id}", response_model=DeleteResponse)
def delete_category(
    db_category: CategoryDB = Depends(get_category_or_404),
    db: Session = Depends(get_db),
):
    category_id = db_category.id

    try:
        db.delete(db_category)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Category still has items assigned to it",
        )
    return {"deleted": category_id}
