from pydantic import BaseModel
from datetime import datetime

class ItemCreate(BaseModel):
    name: str
    price: float
    in_stock: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
    
    class Config:
        from_attributes = True
        
class CategoryCreate(BaseModel):
    name: str
    description: str | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    
    class Config:
        from_attributes = True 
    