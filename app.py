from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from routers import categories, items

app = FastAPI()

app.include_router(items.router)
app.include_router(categories.router)

UNIQUE_VIOLATION = "23505"
FOREIGN_KEY_VIOLATION = "23503"


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    pgcode = getattr(exc.orig, "pgcode", None)
    if pgcode == UNIQUE_VIOLATION:
        return JSONResponse(status_code=409, content={"detail": "Resource already exists"})
    if pgcode == FOREIGN_KEY_VIOLATION:
        return JSONResponse(status_code=400, content={"detail": "Referenced resource does not exist"})
    return JSONResponse(status_code=500, content={"detail": "Database integrity error"})
