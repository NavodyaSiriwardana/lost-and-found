import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)

db = client["user_db"]
user_collection = db["users"]

def serialize_user(user):
    return {
        "id": str(user["_id"]),
        "full_name": user["full_name"],
        "email": user["email"],
        "student_id": user.get("student_id"),
        "role": user.get("role", "Student"),
        "created_at": user.get("created_at")
    }

def get_all_users_db():
    # මුද්‍රණ පදය (password) ආරක්ෂාව සඳහා ලබා නොදේ
    users = user_collection.find({}, {"password": 0})
    return [serialize_user(u) for u in users]

def get_user_by_id_db(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if user:
        return serialize_user(user)
    return None

def find_user_by_email(email: str):
    return user_collection.find_one({"email": email})

def create_user_db(user_data: dict):
    result = user_collection.insert_one(user_data)
    new_user = user_collection.find_one({"_id": result.inserted_id}, {"password": 0})
    return serialize_user(new_user)

def update_user_db(user_id: str, updated_data: dict):
    user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
    updated_user = user_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    return serialize_user(updated_user) if updated_user else None

def delete_user_db(user_id: str):
    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0