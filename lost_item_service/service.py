from bson import ObjectId
from data_service import lost_items_collection

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

def get_all_lost_items():
    items = []
    for item in lost_items_collection.find():
    
        items.append(serialize_doc(item))
    return items

def get_lost_item_by_id(item_id):
    item = lost_items_collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return serialize_doc(item)
    return None

def create_lost_item(item_data):
    result = lost_items_collection.insert_one(item_data)
    new_item = lost_items_collection.find_one({"_id": result.inserted_id})
    return serialize_doc(new_item)

def update_lost_item(item_id, item_data):
    result = lost_items_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": item_data}
    )
    updated_item = lost_items_collection.find_one({"_id": ObjectId(item_id)})
    if updated_item:
        return serialize_doc(updated_item)
    return None

def delete_lost_item(item_id):
    result = lost_items_collection.delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count > 0
    