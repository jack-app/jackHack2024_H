from fastapi import HTTPException
class StateNotExists(HTTPException):
    def __init__(self, state:str|None=None):
        super().__init__(status_code=400, detail=f"State {state} does not exist.")
class TokenFechingTimeout(HTTPException):
    def __init__(self, msg:str|None=None):
        super().__init__(status_code=408, detail=msg or "Token fetching timeout.")