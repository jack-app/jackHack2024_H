from pydantic import BaseModel

class GAPITokenBundle(BaseModel):
    access_token: str
    refgresh_token: str