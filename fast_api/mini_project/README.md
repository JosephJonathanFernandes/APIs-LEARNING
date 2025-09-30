# FastAPI Mini Project

A production-ready FastAPI application demonstrating:
- 🚀 **Async CRUD operations** with SQLAlchemy
- 🔐 **JWT Token Authentication** 
- 🗃️ **SQLite Database** integration
- 🔗 **Dependency Injection** patterns
- 📝 **Pydantic Data Validation**
- 🛡️ **Protected and Public Routes**

## 🏗️ Project Structure

```
mini_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app configuration
│   ├── auth/                # Authentication system
│   │   ├── __init__.py
│   │   ├── security.py      # Password hashing & JWT
│   │   └── dependencies.py  # Auth dependencies
│   ├── database/            # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py    # Database connection
│   │   └── crud.py         # CRUD operations
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   ├── user.py         # SQLAlchemy models
│   │   └── schemas.py      # Pydantic schemas
│   └── routers/            # API endpoints
│       ├── __init__.py
│       ├── auth.py         # Authentication routes
│       ├── users.py        # User CRUD routes
│       └── general.py      # Public routes
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```powershell
# Option 1: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python
python -m app.main
```

### 3. Access the API

- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Welcome Endpoint**: http://localhost:8000/welcome

## 📡 API Endpoints

### Public Endpoints (No Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with app info |
| GET | `/welcome` | Public welcome message |
| GET | `/health` | Health check |
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get token |

### Protected Endpoints (Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/protected` | Protected route demo |
| GET | `/auth/me` | Get current user info |
| GET | `/users/` | List all users |
| GET | `/users/{id}` | Get specific user |
| PUT | `/users/{id}` | Update user (own profile only) |
| DELETE | `/users/{id}` | Delete user (own account only) |

## 🔐 Authentication Flow

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "age": 30,
       "password": "securepassword"
     }'
```

### 2. Login and Get Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john@example.com&password=securepassword"
```

### 3. Use Token for Protected Routes

```bash
curl -X GET "http://localhost:8000/protected" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🧪 Testing the API

### PowerShell Examples

```powershell
# 1. Test welcome endpoint
Invoke-RestMethod -Uri "http://localhost:8000/welcome" -Method GET

# 2. Register a user
$registerData = @{
    name = "Test User"
    email = "test@example.com"
    age = 25
    password = "testpassword"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/auth/register" -Method POST -Body $registerData -ContentType "application/json"

# 3. Login
$loginData = "username=test@example.com&password=testpassword"
$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" -Method POST -Body $loginData -ContentType "application/x-www-form-urlencoded"
$token = $response.access_token

# 4. Access protected route
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Uri "http://localhost:8000/protected" -Method GET -Headers $headers
```

## 🎓 Learning Objectives Achieved

✅ **CRUD Operations**: Full Create, Read, Update, Delete functionality  
✅ **SQLite + SQLAlchemy**: Async database operations with ORM  
✅ **Token Authentication**: JWT-based auth with dependency injection  
✅ **Async Endpoints**: All endpoints use async/await patterns  
✅ **Dependency Injection**: Proper use of FastAPI's Depends system  
✅ **Data Validation**: Pydantic models for request/response validation  
✅ **Error Handling**: Proper HTTP status codes and error messages  
✅ **Security**: Password hashing, token expiration, user permissions  

## 🔧 Key Features Demonstrated

- **Async SQLAlchemy**: Using `AsyncSession` for database operations
- **JWT Authentication**: Secure token-based authentication
- **Dependency Injection**: Reusable dependencies for auth and database
- **Pydantic Schemas**: Type-safe data validation and serialization
- **Router Organization**: Clean separation of concerns with multiple routers
- **Error Handling**: Proper HTTP exceptions and status codes
- **Database Relationships**: User model with proper SQLAlchemy configuration
- **CORS Support**: Cross-origin resource sharing enabled
- **Application Lifespan**: Proper startup and shutdown handling

## 🚀 Next Steps

1. Add more entities (e.g., Posts, Categories)
2. Implement relationships between entities
3. Add pagination and filtering
4. Implement role-based permissions
5. Add rate limiting
6. Add logging and monitoring
7. Add unit and integration tests
8. Deploy to cloud platforms

## 💡 Production Considerations

- Change `SECRET_KEY` in production
- Use environment variables for configuration
- Implement proper logging
- Add rate limiting
- Use HTTPS in production
- Configure CORS properly for production
- Add comprehensive error handling
- Implement database migrations
- Add health checks and monitoring