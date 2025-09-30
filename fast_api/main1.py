from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model
class User(BaseModel):
    name: str
    age: int
    email: str | None = None  # optional field


# POST endpoint accepting JSON body
@app.post("/user/")
def create_user(user: User):
    return {"message": "User created", "user": user}

# New endpoint for welcome message
@app.post("/user/welcome")
def welcome_user(user: User):
    return {"message": f"Welcome, {user.name}!"}
