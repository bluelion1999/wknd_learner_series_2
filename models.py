from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, \
                        func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ItemDB(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    category = relationship("CategoryDB", back_populates="items")
    
class CategoryDB(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    items = relationship("ItemDB", back_populates="category")
    