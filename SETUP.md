# Quick Setup Guide

## Prerequisites

- Python 3.8+ installed
- Node.js 18+ and npm installed

## Backend Setup

1. Install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

2. Run the backend server (from project root):

```bash
cd C:\Users\Dell\Desktop\sweet-shop-kata
uvicorn backend.main:app --reload
```

Or if you're already in the backend directory, run from parent:

```bash
cd ..
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

## Frontend Setup

1. Install Node dependencies:

```bash
cd frontend
npm install
```

2. Run the frontend dev server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Running Tests

Backend tests:

```bash
cd backend
pytest tests/ -v
```

## First Time Setup

1. Start the backend server first
2. Start the frontend server
3. Open `http://localhost:3000` in your browser
4. Register a new user (first user will be a regular user)
5. To create an admin user, you can manually update the database or create a user with role="admin"

## Default Admin User (Optional)

To create an admin user via Python:

```python
from backend.models import User
from backend import auth
from backend.database import engine, Session

with Session(engine) as session:
    admin = User(
        username="admin",
        email="admin@example.com",
        password_hash=auth.get_password_hash("admin123"),
        role="admin"
    )
    session.add(admin)
    session.commit()
```
