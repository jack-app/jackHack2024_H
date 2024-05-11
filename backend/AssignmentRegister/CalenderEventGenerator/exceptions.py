from fastapi import HTTPException

class AssignmentOverDue(HTTPException):
    def __init__(self, msg:str|None = None):
        super().__init__(status_code=400, detail=msg or "Assignment is overdue")