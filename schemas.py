from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    category_id: int | None = None
    in_stock: bool = True
    
    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) ->str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("name must not be blank")
        return stripped


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    category_id: int | None
    in_stock: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) ->str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("name must not be blank")
        return stripped

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeleteResponse(BaseModel):
    deleted: int
