from pymongo import MongoClient
# from dotenv import load_dotenv
import os

# load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["student_manager"]

students_collection = db["students"]
users_collection = db["users"]

students_collection.create_index(
    "name",
    unique = True
)

users_collection.create_index(
    "username",
    unique=True
)
