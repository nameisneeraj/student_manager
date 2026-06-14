from pydantic import BaseModel

class Student(BaseModel):
    name: str 
    age: int
    course: str


class StudentResponse(BaseModel):
    id: str
    name: str
    age: int
    course: str

class CreatStudentResponse(BaseModel):
    message: str
    student: StudentResponse

class StudentListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[StudentResponse]

class UpdateStudentResponse(BaseModel):
    message: str
    student: StudentResponse


class DeleteStudnetResponse(BaseModel):
    message: str
    student_id: str
    student_name: str


class MessageResponse(BaseModel):
    message: str
