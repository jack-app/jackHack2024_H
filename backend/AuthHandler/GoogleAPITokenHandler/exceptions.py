from fastapi import HTTPException

class ReAuthenticationRequired(HTTPException):
    def __init__(self, msg:str):
        super().__init__(status_code=401, detail=msg or "Re-authentication required.")
class TokenNotFound(HTTPException):
    def __init__(self, msg:str):
        super().__init__(status_code=400, detail=msg or "Token not found.")