from pydantic import BaseModel
from shared.Units import Sec

class AssignmentEntry(BaseModel):
    id: str
    title: str
    sourceName: str
    courseId: str
    dueDate: str
    duration: int | None #Sec