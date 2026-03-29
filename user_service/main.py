from fastapi import FastAPI, HTTPException, status
from models import UserCreate, UserUpdate
from service import (
    fetch_all_users,
    fetch_user_by_id,
    register_new_user,
    edit_user,
    remove_user
)

app = FastAPI(title="User Service")

@app.get("/")
def read_root():
    return {"message": "User Service is running on Port 8001"}

@app.post("/api/users/register", status_code=status.HTTP_201_CREATED)
def register_user_endpoint(user: UserCreate):
    new_user = register_new_user(user.dict())
    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return new_user

@app.get("/api/users")
def get_users():
    return {"users": fetch_all_users()}

@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    user = fetch_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/users/{user_id}")
def update_user_endpoint(user_id: str, user: UserUpdate):
    updated = edit_user(user_id, user.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="User not found or no changes made")
    return updated

@app.delete("/api/users/{user_id}")
def delete_user_endpoint(user_id: str):
    if not remove_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}