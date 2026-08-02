from fastapi import FastAPI
from routers import items, categories
import models

app = FastAPI()


app.include_router(items.router)
app.include_router(categories.router)
