from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)

db = client["found_item_service_db"]
collection = db["found_items"]


def serialize_found_item(item):
    return {
        "id": str(item["_id"]),
        "itemName": item["itemName"],
        "description": item["description"],
        "category": item["category"],
        "color": item["color"],
        "locationFound": item["locationFound"],
        "dateFound": item["dateFound"],
        "contactNumber": item["contactNumber"],
        "status": item["status"]
    }


def get_all_found_items():
    items = collection.find()
    return [serialize_found_item(item) for item in items]


def get_found_item_by_id(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return serialize_found_item(item)
    return None


def create_found_item(item_data: dict):
    result = collection.insert_one(item_data)
    new_item = collection.find_one({"_id": result.inserted_id})
    return serialize_found_item(new_item)


def update_found_item(item_id: str, updated_data: dict):
    collection.update_one({"_id": ObjectId(item_id)}, {"$set": updated_data})
    updated_item = collection.find_one({"_id": ObjectId(item_id)})
    if updated_item:
        return serialize_found_item(updated_item)
    return None


def delete_found_item(item_id: str):
    result = collection.delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count > 0