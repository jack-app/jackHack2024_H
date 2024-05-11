from datetime import datetime
from fastapi import HTTPException

class TooManyEvents(HTTPException):
    def __init__(self,msg:str|None = None):
        super().__init__(status_code=500,detail=msg or "There were too many events to handle")
class UnexpectedAPIResponce(Exception): pass
class ReAuthorizationRequired(HTTPException):
    def __init__(self,msg:str|None = None):
        super().__init__(status_code=401,detail=msg or "Reauthorization is required")
class TimeZoneUnspecified(HTTPException):
    def __init__(self, time:datetime):
        super().__init__(status_code=400,detail=f"timezone is not specified in {time.isoformat()}")