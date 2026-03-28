import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)

db = client["claim_db"]
claim_collection = db["claims"]

def serialize_claim(claim):
    return {
        "id": str(claim["_id"]),
        "user_id": claim["user_id"],
        "user_name": claim["user_name"],
        "found_item_id": claim["found_item_id"],
        "item_name": claim["item_name"],
        "proof_description": claim["proof_description"],
        "phone_number": claim["phone_number"],
        "status": claim.get("status", "Pending"),
        "admin_comments": claim.get("admin_comments")
    }

def get_all_claims_db():
    claims = claim_collection.find()
    return [serialize_claim(c) for c in claims]

def get_claim_by_id_db(claim_id: str):
    claim = claim_collection.find_one({"_id": ObjectId(claim_id)})
    if claim:
        return serialize_claim(claim)
    return None

def create_claim_db(claim_data: dict):
    result = claim_collection.insert_one(claim_data)
    new_claim = claim_collection.find_one({"_id": result.inserted_id})
    return serialize_claim(new_claim)

def update_claim_db(claim_id: str, updated_data: dict):
    claim_collection.update_one({"_id": ObjectId(claim_id)}, {"$set": updated_data})
    updated_item = claim_collection.find_one({"_id": ObjectId(claim_id)})
    return serialize_claim(updated_item) if updated_item else None

def delete_claim_db(claim_id: str):
    result = claim_collection.delete_one({"_id": ObjectId(claim_id)})
    return result.deleted_count > 0