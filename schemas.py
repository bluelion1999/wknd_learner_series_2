from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ItemCreate(BaseModel):
    name: str
    price: float
    category_id: int | None = None
    in_stock: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    category_id: int | None
    in_stock: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
        
class CategoryCreate(BaseModel):
    name: str
    description: str | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    