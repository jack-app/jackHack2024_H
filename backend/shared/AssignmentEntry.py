from pydantic import BaseModel

class AssignmentEntry(BaseModel):
    id: str | None
    title: str | None
    sourseName: str| None
    courseId: str | None
    dueData: str | None
    duration: int | None #sec