from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import ItemDB
from schemas import DeleteResponse, ItemCreate, ItemResponse

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemResponse])
def list_items(db: Session = Depends(get_db)):
    db_items = db.execute(select(ItemDB)).scalars().all()
    return db_items


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.get(ItemDB, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.post("", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemDB(
        name=item.name,
        price=item.price,
        category_id=item.category_id,
        in_stock=item.in_stock,
    )
    try:
        db.add(db_item)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category does not exist")
    db.refresh(db_item)
    return db_item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.get(ItemDB, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item.name
    db_item.price = item.price
    db_item.category_id = item.category_id
    db_item.in_stock = item.in_stock

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category does not exist")
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}", response_model=DeleteResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.get(ItemDB, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"deleted": item_id}
