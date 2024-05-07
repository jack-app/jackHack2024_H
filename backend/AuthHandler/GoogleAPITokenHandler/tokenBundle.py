from .literals import REFRESH_TOKEN, ACCESS_TOKEN
from DEPLOY_SETTING import CLIENT_ID, CLIENT_SECRET
from .exceptions import TokenNotFound, ReAuthenticationRequired
from aiohttp import request
from google.auth.transport.requests import Request as GRequest
from google.auth.exceptions import RefreshError


class GoogleAPITokenBundle:
    @staticmethod
    def from_dict(d: dict):
        try:
            return GoogleAPITokenBundle(d[ACCESS_TOKEN], d[REFRESH_TOKEN])
        except KeyError as e:
            raise TokenNotFound(e)

    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET

    async def revoke(self):
        await request(
            "POST", 
            "https://oauth2.googleapis.com/revoke", 
            headers = {'content-type': 'application/x-www-form-urlencoded'},
            params={'token': self.refresh_token}
        )
        self.access_token = None
        self.refresh_token = None
        return
    
    async def refresh(self):
        try:
            async with request(
                "POST",
                "https://oauth2.googleapis.com/token",
                headers={'content-type': 'application/x-www-form-urlencoded'},
                data={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'refresh_token': self.refresh_token,
                    'grant_type': 'refresh_token'
                }
            ) as resp:
                self.access_token = (await resp.json())['access_token']
        except RefreshError as e:
            raise ReAuthenticationRequired("token-refresh failed. please re-authenticate.")
