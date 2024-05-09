from pydantic import BaseModel
class AssignmentEntry(BaseModel):
    id: str
    title: str
    courseName: str
    courseId: str
    dueDate: str
    duration: int #Min