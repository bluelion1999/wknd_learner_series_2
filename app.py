from fastapi import FastAPI
from database import engine, Base
from routers import items
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(items.router)
