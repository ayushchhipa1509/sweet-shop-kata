from fastapi import FastAPI
from .routes import auth

app = FastAPI(title="Sweet Shop Management System")

app.include_router(auth.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
