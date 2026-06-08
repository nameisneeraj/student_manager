from pymongo import MongoClient

client = MongoClient("mongodb+srv://studentadmin:Neeraj10010@student-api-cluster.quwxlfz.mongodb.net/?appName=student-api-cluster")

db = client["student_manager"]

student_collections = db["students"]

student_collections.create_index(
    "name",
    unique = True
)
