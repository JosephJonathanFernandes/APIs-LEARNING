from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import async_engine
from .models.user import Base
from .routers import auth_router, users_router, general_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - setup and cleanup"""
    # Create database tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup if needed
    await async_engine.dispose()

# Create FastAPI app
app = FastAPI(
    title="FastAPI Mini Project",
    description="A production-ready FastAPI application with CRUD operations, SQLite database, JWT authentication, and async endpoints",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(general_router)
app.include_router(auth_router)
app.include_router(users_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)