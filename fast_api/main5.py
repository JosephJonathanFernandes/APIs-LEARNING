from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# DB Model
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Pydantic model
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str | None = None

# Create user
@app.post("/users/")
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = UserDB(name=user.name, age=user.age, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read all users
@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()
