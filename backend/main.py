from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import auth, sweets
from .database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: (if needed, add cleanup here)


app = FastAPI(
    title="Sweet Shop Management System",
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(sweets.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
