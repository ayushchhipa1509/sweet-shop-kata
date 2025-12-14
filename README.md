# Sweet Shop Management System

A full-stack web application for managing a sweet shop with user authentication, sweet inventory management, and purchase functionality.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Role-Based Access**: Admin and regular user roles
- **Sweet Management**: CRUD operations for sweets (admin-only creation)
- **Purchase System**: Public purchase endpoint that decreases inventory
- **Modern Frontend**: React + TypeScript + Vite with beautiful UI
- **RESTful API**: FastAPI backend with SQLModel

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLModel**: SQL database ORM
- **SQLite**: Database
- **JWT**: Authentication tokens
- **Pytest**: Testing framework

### Frontend
- **React 18**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool
- **React Router**: Navigation
- **React Query**: Data fetching
- **Axios**: HTTP client

## Project Structure

```
sweet-shop-kata/
├── backend/
│   ├── models.py          # Database models (User, Sweet)
│   ├── database.py        # Database connection and session
│   ├── auth.py            # JWT and password hashing
│   ├── deps.py            # FastAPI dependencies (get_current_user)
│   ├── main.py            # FastAPI app and routes
│   ├── schemas.py         # Pydantic schemas
│   ├── routes/
│   │   ├── auth.py        # Authentication endpoints
│   │   └── sweets.py      # Sweets CRUD endpoints
│   └── tests/
│       ├── conftest.py    # Pytest fixtures
│       ├── test_models.py # Model tests
│       ├── test_auth.py   # Authentication tests
│       └── test_sweets.py # Sweets API tests
└── frontend/
    ├── src/
    │   ├── pages/         # Login, Register, Dashboard
    │   ├── components/    # SweetCard, AddSweetModal
    │   ├── api.ts         # API client
    │   └── App.tsx        # Main app component
    └── package.json
```

## Setup Instructions

### Backend Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn sqlmodel python-jose passlib bcrypt python-multipart
```

2. Run the backend:
```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the frontend:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Sweets
- `GET /sweets` - Get all sweets (public)
- `POST /sweets` - Create a new sweet (admin only)
- `POST /sweets/{id}/purchase` - Purchase a sweet (public, decreases quantity)

### Health
- `GET /health` - Health check endpoint

## Testing

Run backend tests:
```bash
cd backend
pytest tests/ -v
```

For HTML test report (requires pytest-html):
```bash
pip install pytest-html
pytest tests/ --html=report.html --self-contained-html
```

## My AI Usage

Throughout this project, I used AI assistance (ChatGPT) to:

1. **Phase 1 - Project Setup**: Set up the initial FastAPI project structure with health check endpoint.

2. **Phase 2 - Database Models**: 
   - Created SQLModel models for User and Sweet entities
   - Set up database connection with SQLite
   - Implemented test fixtures with in-memory database for test isolation
   - AI helped with model definitions and test structure

3. **Phase 3 - Authentication**:
   - Implemented JWT token generation and validation
   - Created password hashing with bcrypt
   - Built registration and login endpoints
   - Created authentication tests
   - AI assisted with JWT implementation and security best practices

4. **Phase 4 - Sweets API**:
   - Created CRUD endpoints for sweets
   - Implemented purchase logic with quantity management
   - Added role-based access control (admin-only creation)
   - Created reusable dependencies (deps.py) for authentication
   - AI helped with FastAPI dependency injection patterns

5. **Phase 5 - Frontend**:
   - Set up React + TypeScript + Vite project
   - Created Login, Register, and Dashboard pages
   - Implemented React Query for data fetching
   - Built SweetCard and AddSweetModal components
   - Added routing with React Router
   - AI assisted with React patterns, TypeScript types, and UI design

6. **Bug Fixes**:
   - Fixed client fixture in conftest.py
   - Fixed token expiration to use ACCESS_TOKEN_EXPIRE_MINUTES constant
   - Added database initialization on startup
   - Updated .gitignore for Python project

**AI Co-author**: ChatGPT was used as a pair programming partner throughout the development process, helping with code structure, best practices, and implementation details.

## Screenshots

Please add screenshots of:
1. Login page
2. Dashboard with sweets
3. Admin "Add Sweet" modal

## Future Improvements

- [ ] Add user profile page
- [ ] Implement sweet editing and deletion (admin)
- [ ] Add order history
- [ ] Implement pagination for sweets list
- [ ] Add search and filter functionality
- [ ] Deploy to production
- [ ] Add Docker configuration
- [ ] Implement proper JWT token refresh
- [ ] Add email verification
- [ ] Add unit tests for frontend components

## License

This project is part of an AI Kata exercise.
