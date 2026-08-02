from pydantic import BaseModel

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