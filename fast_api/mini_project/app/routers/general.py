from fastapi import APIRouter, Depends
from datetime import datetime
from ..auth import get_current_active_user

router = APIRouter(tags=["General"])

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI Mini Project!",
        "description": "A production-ready FastAPI app with CRUD, SQLite, JWT auth, and async endpoints",
        "timestamp": datetime.utcnow(),
        "endpoints": {
            "auth": "/auth",
            "users": "/users", 
            "welcome": "/welcome",
            "protected": "/protected",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@router.get("/welcome")
async def welcome():
    """Public welcome endpoint - no authentication required"""
    return {
        "message": "Welcome to our FastAPI application!",
        "status": "public",
        "description": "This endpoint is accessible without authentication",
        "features": [
            "✅ SQLite database with SQLAlchemy",
            "✅ Async endpoints", 
            "✅ JWT token authentication",
            "✅ CRUD operations",
            "✅ Dependency injection",
            "✅ Pydantic data validation",
            "✅ API documentation"
        ]
    }

@router.get("/protected")
async def protected_route(current_user = Depends(get_current_active_user)):
    """Protected endpoint - requires authentication"""
    return {
        "message": f"Hello {current_user.name}! This is a protected route.",
        "status": "protected",
        "user_info": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "is_active": current_user.is_active
        },
        "description": "This endpoint requires a valid JWT token"
    }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "service": "FastAPI Mini Project"
    }