from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker



DATABASE_URL = "postgresql://apiuser:apipass@db:5432/apidb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


Base = declarative_base()

class ItemDB(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    
    
Base.metadata.create_all(bind=engine)    


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


