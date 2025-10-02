# Enhanced Flask REST API Documentation

## 🚀 Features

- ✅ **Proper HTTP Status Codes** (200, 201, 400, 404, 422, 500)
- ✅ **Input Validation** with detailed error messages
- ✅ **Standardized Error Handling**
- ✅ **Pagination** with metadata
- ✅ **SQLite Database** with SQLAlchemy ORM
- ✅ **JWT Authentication** for secure sessions
- ✅ **API Key Authentication** for machine-to-machine access
- ✅ **Soft Delete** (users marked inactive vs. permanent deletion)

## 📚 API Endpoints

### Base URL
```
http://127.0.0.1:5000
```

---

## 🔐 Authentication

### 1. Register User
**POST** `/auth/register`

Create a new user account with password authentication.

**Request Body:**
```json
{
  "name": "Joseph Fernandes",
  "email": "joseph@example.com",
  "password": "secure123"
}
```

**Response (201):**
```json
{
  "error": false,
  "status_code": 201,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "name": "Joseph Fernandes",
    "email": "joseph@example.com",
    "created_at": "2025-10-03T10:30:00"
  }
}
```

---

### 2. Login User
**POST** `/auth/login`

Login and receive JWT token for authentication.

**Request Body:**
```json
{
  "email": "joseph@example.com",
  "password": "secure123"
}
```

**Response (200):**
```json
{
  "error": false,
  "status_code": 200,
  "message": "Login successful",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
      "id": 1,
      "name": "Joseph Fernandes",
      "email": "joseph@example.com"
    }
  }
}
```

---

### 3. Generate API Key
**POST** `/auth/api-key`

Generate API key for machine-to-machine authentication (requires JWT token).

**Headers:**
```
Authorization: Bearer your-jwt-token
```

**Response (200):**
```json
{
  "error": false,
  "status_code": 200,
  "message": "API key generated successfully",
  "data": {
    "api_key": "abc123def456...",
    "message": "Use this key in X-API-Key header for authentication"
  }
}
```

---

### 4. Get Profile (Protected)
**GET** `/auth/profile`

Get current user's profile information.

**Headers:**
```
Authorization: Bearer your-jwt-token
```

**Response (200):**
```json
{
  "error": false,
  "status_code": 200,
  "data": {
    "id": 1,
    "name": "Joseph Fernandes",
    "email": "joseph@example.com",
    "created_at": "2025-10-03T10:30:00",
    "updated_at": "2025-10-03T10:30:00",
    "is_active": true
  }
}
```

---

### 5. Update Profile (Protected)
**PUT** `/auth/profile`

Update current user's profile.

**Headers:**
```
Authorization: Bearer your-jwt-token
```

**Request Body:**
```json
{
  "name": "Joseph J. Fernandes",
  "email": "jjf@example.com"
}
```

---

## 👥 User Management

### 1. Get All Users (with Pagination)
**GET** `/users?page=1&per_page=10`

Retrieve paginated list of users.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (1-100, default: 10)

**Authentication:** Optional (JWT or API Key)

**Headers (for API Key auth):**
```
X-API-Key: your-api-key
```

**Response (200):**
```json
{
  "error": false,
  "status_code": 200,
  "data": [
    {
      "id": 1,
      "name": "Joseph Fernandes",
      "email": "joseph@example.com",
      "created_at": "2025-10-03T10:30:00",
      "updated_at": "2025-10-03T10:30:00",
      "is_active": true
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total": 1,
    "pages": 1,
    "has_next": false,
    "has_prev": false,
    "next_page": null,
    "prev_page": null,
    "authenticated": true
  }
}
```

---

### 2. Get Single User
**GET** `/users/{id}`

Get specific user by ID.

**Response (200):**
```json
{
  "error": false,
  "status_code": 200,
  "data": {
    "id": 1,
    "name": "Joseph Fernandes",
    "email": "joseph@example.com",
    "created_at": "2025-10-03T10:30:00",
    "updated_at": "2025-10-03T10:30:00",
    "is_active": true
  }
}
```

---

### 3. Create User
**POST** `/users`

Create a new user (without password - for basic user records).

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Response (201):**
```json
{
  "error": false,
  "status_code": 201,
  "message": "User created successfully",
  "data": {
    "id": 2,
    "name": "Jane Doe",
    "email": "jane@example.com",
    "created_at": "2025-10-03T11:00:00",
    "updated_at": "2025-10-03T11:00:00",
    "is_active": true
  }
}
```

---

### 4. Update User
**PUT** `/users/{id}`

Update user information.

**Request Body:**
```json
{
  "name": "Jane Smith",
  "email": "jane.smith@example.com"
}
```

**Response (200):**
```json
{
  "error": false,
  "status_code": 200,
  "message": "User updated successfully",
  "data": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "created_at": "2025-10-03T11:00:00",
    "updated_at": "2025-10-03T11:15:00",
    "is_active": true
  }
}
```

---

### 5. Delete User
**DELETE** `/users/{id}`

Soft delete user (marks as inactive).

**Response (204):**
```json
{
  "error": false,
  "status_code": 204,
  "message": "User deleted successfully"
}
```

---

## ❌ Error Responses

All error responses follow this format:

```json
{
  "error": true,
  "message": "Error description",
  "status_code": 400,
  "errors": ["Detailed error 1", "Detailed error 2"]
}
```

### Common Error Codes:

- **400 Bad Request** - Malformed request or missing required data
- **401 Unauthorized** - Invalid credentials or missing authentication
- **404 Not Found** - Resource not found
- **422 Unprocessable Entity** - Validation errors
- **500 Internal Server Error** - Server-side error

### Validation Errors Example:
```json
{
  "error": true,
  "message": "Validation failed",
  "status_code": 422,
  "errors": [
    "name is required",
    "Invalid email format",
    "Email must be unique"
  ]
}
```

---

## 🔧 Testing Examples

### Using PowerShell (Invoke-WebRequest):

**Register User:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/auth/register" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"name": "Test User", "email": "test@example.com", "password": "password123"}'
```

**Login:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/auth/login" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"email": "test@example.com", "password": "password123"}'
```

**Get Users with Pagination:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/users?page=1&per_page=5" -Method GET
```

**Create User:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/users" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"name": "New User", "email": "new@example.com"}'
```

**Using JWT Token:**
```powershell
$token = "your-jwt-token-here"
Invoke-WebRequest -Uri "http://127.0.0.1:5000/auth/profile" -Method GET -Headers @{"Authorization"="Bearer $token"}
```

**Using API Key:**
```powershell
$apiKey = "your-api-key-here"
Invoke-WebRequest -Uri "http://127.0.0.1:5000/users" -Method GET -Headers @{"X-API-Key"="$apiKey"}
```

---

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app_enhanced.py
   ```

3. **Test the endpoints:**
   - Visit: http://127.0.0.1:5000
   - Register a user: POST `/auth/register`
   - Login to get JWT: POST `/auth/login`
   - Test protected routes with your JWT token

---

## 🔒 Security Notes

- Change `SECRET_KEY` and `JWT_SECRET_KEY` in production
- Use HTTPS in production
- Implement rate limiting for production use
- Consider adding refresh tokens for better JWT security
- Store API keys securely and rotate them regularly