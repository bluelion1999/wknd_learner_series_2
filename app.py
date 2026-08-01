from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, ItemDB

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).all()
    return db_item
    
@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/items")
def post_items(item: Item, db: Session = Depends(get_db)):
    db_item = ItemDB(name=item.name, price=item.price, in_stock=item.in_stock)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        db.delete(db_item)
        db.commit()
        return {"deleted":item_id}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.name = item.name
    db_item.price = item.price
    db_item.in_stock = item.in_stock
    
    db.commit()
    db.refresh(db_item)
    return db_item    
        