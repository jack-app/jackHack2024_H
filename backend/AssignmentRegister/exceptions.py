from datetime import datetime
from fastapi import HTTPException

class InvalidToken(HTTPException):
    def __init__(self,msg:str):
        super().__init__(status_code=401,detail=msg)
class TooManyEvents(HTTPException):
    def __init__(self,msg:str):
        super().__init__(status_code=500,detail=msg)
class UnexpectedAPIResponce(Exception): pass
class ReAuthorizationRequired(HTTPException):
    def __init__(self,msg:str):
        super().__init__(status_code=401,detail=msg)
class TimeZoneUnspecified(HTTPException):
    def __init__(self, time:datetime):
        super().__init__(status_code=400,detail=f"timezone is not specified in {time.isoformat()}")