from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ItemDB
from schemas import ItemCreate, ItemResponse

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).all()
    return db_item
    
@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.post("", response_model=ItemResponse)
def post_items(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemDB(name=item.name, price=item.price, in_stock=item.in_stock)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.name = item.name
    db_item.price = item.price
    db_item.in_stock = item.in_stock
    
    db.commit()
    db.refresh(db_item)
    return db_item    
        
@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        db.delete(db_item)
        db.commit()
        return {"deleted":item_id}