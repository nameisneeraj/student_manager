from pymongo import MongoClient

client = MongoClient("mongodb+srv://studentadmin:Neeraj10010@student-api-cluster.quwxlfz.mongodb.net/?appName=student-api-cluster")

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
