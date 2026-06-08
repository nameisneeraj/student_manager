from pydantic import BaseModel

class Student(BaseModel):
    name: str 
    age: int
    course: str


class StudentResponse(BaseModel):
    name: str
    age: int
    course: str
    