from fastapi import FastAPI
from database import engine, Base
from routers import items, categories
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(items.router)
app.include_router(categories.router)
