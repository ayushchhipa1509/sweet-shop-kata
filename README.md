# Sweet Shop Management System

A full-stack web application for managing a sweet shop with user authentication, sweet inventory management, and purchase functionality. Built with FastAPI (backend) and React + TypeScript (frontend).

## 🚀 Features

- **User Authentication**: JWT-based authentication with registration and login
- **Role-Based Access Control**: Admin and regular user roles
  - First registered user automatically becomes admin
  - Admins can delete sweets and view statistics
  - All authenticated users can create sweets
- **Sweet Management**:
  - View all sweets (public)
  - Create new sweets (authenticated users)
  - Delete sweets (admin only)
  - Purchase sweets (decreases inventory)
- **User Profile**:
  - View user information
  - Admin dashboard with statistics (total sweets, in stock, out of stock)
  - Display user permissions
- **Modern Frontend**: React + TypeScript + Vite with beautiful, responsive UI
- **RESTful API**: FastAPI backend with SQLModel ORM

## 🛠️ Tech Stack

### Backend

- **FastAPI** 0.115.0 - Modern Python web framework
- **SQLModel** 0.0.22 - SQL database ORM
- **SQLite** - Database
- **JWT** (python-jose) - Authentication tokens
- **Passlib** (bcrypt) - Password hashing
- **Pytest** - Testing framework
- **Uvicorn** - ASGI server

### Frontend

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router DOM** - Navigation
- **React Query** (@tanstack/react-query) - Data fetching and caching
- **Axios** - HTTP client

## 📁 Project Structure

```
sweet-shop-kata/
├── backend/
│   ├── models.py          # Database models (User, Sweet)
│   ├── database.py        # Database connection and session
│   ├── auth.py            # JWT and password hashing utilities
│   ├── deps.py            # FastAPI dependencies (get_current_user, get_current_admin_user)
│   ├── main.py            # FastAPI app, CORS, and route registration
│   ├── schemas.py         # Pydantic schemas for request/response validation
│   ├── requirements.txt   # Python dependencies
│   ├── routes/
│   │   ├── auth.py        # Authentication endpoints (register, login, /me)
│   │   └── sweets.py      # Sweets CRUD endpoints
│   └── tests/
│       ├── conftest.py    # Pytest fixtures and test configuration
│       ├── test_models.py # Database model tests
│       ├── test_auth.py   # Authentication API tests
│       └── test_sweets.py # Sweets API tests
└── frontend/
    ├── src/
    │   ├── pages/         # Login, Register, Dashboard, Profile
    │   ├── components/    # SweetCard, AddSweetModal
    │   ├── api.ts         # API client with axios
    │   └── App.tsx        # Main app component with routing
    ├── package.json       # Node.js dependencies
    └── vite.config.ts     # Vite configuration
```

## 🚦 Quick Start

### Prerequisites

- **Python 3.8+** installed
- **Node.js 18+** and npm installed

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Run the backend server:

```bash
uvicorn main:app --reload
```

The API will be available at:

- **API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc`

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install Node.js dependencies:

```bash
npm install
```

3. Run the frontend development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### First Time Usage

1. **Start the backend server first** (from `backend/` directory)
2. **Start the frontend server** (from `frontend/` directory)
3. Open `http://localhost:3000` in your browser
4. **Register a new user** - The first registered user will automatically become an admin
5. **Login** with your credentials
6. Start creating and managing sweets!

## 📡 API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
  - Request body: `{username, email, password}`
  - Returns: User object with role (first user = admin)
- `POST /auth/login` - Login and get JWT token
  - Form data: `username`, `password`
  - Returns: `{access_token, token_type}`
- `GET /auth/me` - Get current user information (requires authentication)
  - Returns: User object with role

### Sweets

- `GET /sweets` - Get all sweets (public, no authentication required)
- `POST /sweets` - Create a new sweet (requires authentication)
  - Request body: `{name, category, price, quantity}`
- `DELETE /sweets/{id}` - Delete a sweet (admin only)
- `POST /sweets/{id}/purchase` - Purchase a sweet (public, decreases quantity by 1)

### Health

- `GET /health` - Health check endpoint

## 🧪 Testing

### Backend Tests

Run all tests:

```bash
cd backend
pytest tests/ -v
```

Run specific test file:

```bash
pytest tests/test_auth.py -v
```

Generate HTML test report:

```bash
pip install pytest-html
pytest tests/ --html=report.html --self-contained-html
```

### Test Coverage

The test suite includes:

- Database model tests (User, Sweet creation)
- Authentication tests (registration, login, token validation)
- Sweets API tests (CRUD operations, purchase logic, authorization)

## 🎨 Features in Detail

### User Roles

**Admin User:**

- Can create sweets
- Can delete sweets
- Can view admin dashboard with statistics
- First registered user automatically becomes admin

**Regular User:**

- Can create sweets
- Can view and purchase sweets
- Cannot delete sweets

### Profile Page

- View user information (username, email, user ID, role)
- Admin users see:
  - Statistics dashboard (total sweets, items in stock, out of stock)
  - List of admin permissions
- Regular users see their permissions list

## 🔧 Development

### Running in Development Mode

Both backend and frontend support hot-reload:

- Backend: `uvicorn main:app --reload` (auto-reloads on file changes)
- Frontend: `npm run dev` (Vite HMR enabled)

### Database

The application uses SQLite database (`sweets.db` in the backend directory). The database is automatically created on first startup.

To reset the database:

1. Stop the backend server
2. Delete `backend/sweets.db`
3. Restart the backend server (database will be recreated)

## 📝 My AI Usage

Throughout this project, I used AI assistance (ChatGPT) as a pair programming partner:

### Phase 1 - Project Setup

- Set up the initial FastAPI project structure
- Created health check endpoint
- Configured project structure and dependencies

### Phase 2 - Database Models & Core Logic

- Created SQLModel models for User and Sweet entities
- Set up database connection with SQLite
- Implemented test fixtures with in-memory database for test isolation
- AI helped with model definitions, relationships, and test structure

### Phase 3 - Authentication System

- Implemented JWT token generation and validation
- Created password hashing with bcrypt (passlib)
- Built registration and login endpoints
- Created `/auth/me` endpoint for user info
- Added first-user-admin logic
- Created comprehensive authentication tests
- AI assisted with JWT implementation, security best practices, and token handling

### Phase 4 - Sweets API

- Created CRUD endpoints for sweets
- Implemented purchase logic with quantity management
- Added role-based access control
- Created DELETE endpoint for admins
- Created reusable dependencies (deps.py) for authentication
- AI helped with FastAPI dependency injection patterns, error handling, and API design

### Phase 5 - Frontend Implementation

- Set up React + TypeScript + Vite project
- Created Login, Register, Dashboard, and Profile pages
- Implemented React Query for data fetching and caching
- Built SweetCard and AddSweetModal components
- Added routing with React Router
- Implemented JWT token storage and API interceptors
- Added CORS configuration
- AI assisted with React patterns, TypeScript types, UI/UX design, and state management

### Phase 6 - Additional Features

- Added user profile page with admin dashboard
- Implemented delete functionality for sweets
- Added statistics display for admins
- Fixed import issues and module resolution
- Resolved CORS configuration
- Updated .gitignore for proper file exclusions

### Bug Fixes

- Fixed client fixture in conftest.py
- Fixed token expiration to use ACCESS_TOKEN_EXPIRE_MINUTES constant
- Added database initialization on startup
- Resolved ModuleNotFoundError issues
- Fixed CORS middleware configuration
- Updated .gitignore for Python and Node.js projects

**AI Co-author**: ChatGPT was used as a pair programming partner throughout the development process, helping with code structure, best practices, implementation details, debugging, and architectural decisions.

## 📸 Screenshots

The application includes:

1. **Login Page** - User authentication interface
2. **Register Page** - New user registration
3. **Dashboard** - Main sweets display with purchase functionality
4. **Profile Page** - User information and admin dashboard (for admins)
5. **Add Sweet Modal** - Form to create new sweets
6. **Sweet Cards** - Individual sweet display with purchase/delete buttons

## 🔮 Future Improvements

- [x] Add user profile page
- [x] Implement sweet deletion (admin)
- [ ] Add sweet editing functionality
- [ ] Add order history for users
- [ ] Implement pagination for sweets list
- [ ] Add search and filter functionality
- [ ] Add sweet categories management
- [ ] Implement proper JWT token refresh mechanism
- [ ] Add email verification
- [ ] Add unit tests for frontend components
- [ ] Add Docker configuration for easy deployment
- [ ] Deploy to production (Heroku, Vercel, etc.)
- [ ] Add image upload for sweets
- [ ] Implement shopping cart functionality
- [ ] Add order management system

## 📄 License

This project is part of an AI Kata exercise.

## 👤 Author

Developed with AI assistance (ChatGPT) as part of a learning exercise.

## 🔗 Repository

GitHub: https://github.com/ayushchhipa1509/sweet-shop-kata

---

**Note**: Make sure to start the backend server before the frontend for the application to work properly. The frontend expects the API to be running on `http://localhost:8000`.
