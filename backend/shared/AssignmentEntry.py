from pydantic import BaseModel
from shared.Units import Sec

class AssignmentEntry(BaseModel):
    id: str
    title: str
    sourseName: str
    courseId: str
    dueData: str
    duration: Sec | None