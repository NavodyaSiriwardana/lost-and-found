import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "lostDB")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "lost_items")

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
db = client[DATABASE_NAME]
lost_items_collection = db[COLLECTION_NAME]
