from pydantic import BaseModel


class GAPITokenBundle(BaseModel):
    access_token: str
    refresh_token: str
