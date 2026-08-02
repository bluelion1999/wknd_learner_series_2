from fastapi import FastAPI

from routers import categories, items

app = FastAPI()

app.include_router(items.router)
app.include_router(categories.router)
