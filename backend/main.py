import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add project root to Python path if not already there
# This MUST be done before any backend imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from backend.routes import auth, sweets
from backend.database import create_db_and_tables


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
