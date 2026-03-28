import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# .env ෆයිල් එක කියවීම
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

# MongoDB වෙත සම්බන්ධ වීම (Async)
client = AsyncIOMotorClient(MONGO_URL)

# Database එක සහ Collection එක නිර්මාණය වීම (Lazy Creation)
db = client["claim_db"]
claim_collection = db["claims"]