from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic model
class User(BaseModel):
    name: str
    age: int
    email: str | None = None

# In-memory "database"
users = {}

# ✅ Create user
@app.post("/users/{user_id}")
def create_user(user_id: int, user: User):
    if user_id in users:
        raise HTTPException(status_code=400, detail="User ID already exists")
    users[user_id] = user
    return {"message": "User created", "user": user}

# ✅ Read user
@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

# ✅ Update user
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = user
    return {"message": "User updated", "user": user}

# ✅ Delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = users.pop(user_id)
    return {"message": "User deleted", "user": deleted_user}

# ✅ List all users
@app.get("/users/")
def list_users():
    return users
