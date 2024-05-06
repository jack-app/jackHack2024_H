from .literals import REFRESH_TOKEN, ACCESS_TOKEN
from DEPLOY_SETTING import CLIENT_ID, CLIENT_SECRET
from .exceptions import TokenNotFound, ReAuthenticationRequired
from google.oauth2.credentials import Credentials
import requests
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
        self.cred = Credentials(
            self.access_token,
            refresh_token=self.refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )

    def asCredentials(self):
        return self.cred

    def revoke(self):
        requests.post('https://oauth2.googleapis.com/revoke',
            params={'token': self.access_token},
            headers = {'content-type': 'application/x-www-form-urlencoded'})

    def refresh(self):
        try:
            self.cred.refresh(GRequest())
        except RefreshError as e:
            raise ReAuthenticationRequired("token-refresh failed. please re-authenticate.")
