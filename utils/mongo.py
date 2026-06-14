# utils/mongo.py
from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId

def get_object_id(student_id: str):
    try:
        return ObjectId(student_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid Student ID"
        )
    
def serialize_student(student: dict):
    student["id"] = str(student.pop("_id"))
    return student