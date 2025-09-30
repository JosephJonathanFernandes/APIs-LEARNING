from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database URL for SQLite
SQLITE_DATABASE_URL = "sqlite:///./app.db"
ASYNC_SQLITE_DATABASE_URL = "sqlite+aiosqlite:///./app.db"

# Create engines
engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
async_engine = create_async_engine(ASYNC_SQLITE_DATABASE_URL, echo=True)

# Create session factories
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()

# Dependency to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Sync version for initial setup
def get_sync_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()