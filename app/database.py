import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

if not MONGO_URI:
    raise ValueError("MONGODB_URI not found in .env file!")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

db = client.get_default_database()

product_collection = db.get_collection("products")
user_collection = db.get_collection("users")