import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request as GRequest
import requests
from shared.Exceptions import ReAuthentificationNeededException
from shared.Units import MilliSec
from shared.GAPITokenBundle import GAPITokenBundle
from google.auth.exceptions import RefreshError
from datetime import datetime
import asyncio
import secrets
from google.auth.exceptions import InvalidGrantError

load_dotenv('./GoogleAPITokenHandler/.env')

AUTH_FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            './GoogleAPITokenHandler/credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )
AUTH_FLOW.redirect_uri = os.environ['REDIRECT_URI']

ACCESS_TOKEN = "access_token"
REFRESH_TOKEN = "refresh_token"
AUTH_FLOW_STATE = "auth_flow_state"

class _SignQueue:
    def __init__(self, authFlow_abandoned_by = datetime.timedelta(minutes=5)):
        self.records = {}
        self.authFlow_abandoned_by = authFlow_abandoned_by
    def put(self, state: str, authFlow: 'AuthFlowSource'):
        self.records[state]= (authFlow,datetime.datetime.now())

        if len(self.records) > 50:
            asyncio.create_task(self.clean_up())
    def get(self, state):
        response = self.records[state][0]
        return response
    def remove(self, state):
        del self.records[state]
    async def clean_up(self):
        for key in self.records.keys():
            try:
                if datetime.datetime.now() - self.records[key][1] > self.authFlow_abandoned_by:
                    del self.records[key]
                await asyncio.sleep(0.1)
            except KeyError:
                pass

class AuthFlowSource:
    SIGN_QUEUE = _SignQueue()

    def __init__(self):
        self.code = None
        self.state = secrets.token_hex()
        self.result = None

    def sign(state: str, code: str):
        """
        queueにtokenGetterとstateの組が登録されていれば、これにコードをひもづける。
        失敗した場合はValueErrorを返す。
        """
        target = AuthFlowSource.SIGN_QUEUE.get(state)
        if target is None:
            raise ValueError(
                f"designated state: '{state}' is not found in queue: '{AuthFlowSource.SIGN_QUEUE.keys()}'"
            )
        else:
            target.code = code
            return

    async def issue_gapi_tokens(self, timeout: MilliSec = MilliSec(10000), interval: MilliSec = MilliSec(1000)) -> GAPITokenBundle:
        """
        トークンを取得する。
        Timeoutの場合はTimeoutErrorを返す。
        取得結果はキャッシュされる。
        """
        if self.result is not None:
            return self.result

        for _ in range(int(timeout / interval) + 1):
            if self.code is not None:
                break
            await asyncio.sleep(interval.toSec())
        
        if self.code is None:
            raise TimeoutError("timeout. code is not set.")
        
        try:
            tokens = AUTH_FLOW.fetch_token(code=self.code)
            self.result = GAPITokenBundle(
                access_token=tokens["access_token"], 
                refresh_token=tokens["refresh_token"]
            )
        except InvalidGrantError:
            raise ReAuthentificationNeededException("given code was invalid. please re-authenticate.")
        return self.result

    def get_oauth_url(self) -> str:
        authorization_url, state = AUTH_FLOW.authorization_url(
            accsess_type='offline',
            include_granted_scopes='true',
            approval_prompt='force',
            state=self.state
        )
        AuthFlowSource.SIGN_QUEUE.put(state,self)
        return authorization_url


def construct_cledentials(
    tokenBundle: GAPITokenBundle
):
def construct_cledentials(access_token,refresh_token):
    return google.oauth2.credentials.Credentials(
        access_token,
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET']
    )

def revoke(access_token):
    requests.post('https://oauth2.googleapis.com/revoke',
        params={'token': access_token},
        headers = {'content-type': 'application/x-www-form-urlencoded'})

def refresh(cred: google.oauth2.credentials.Credentials):
    try:
        cred.refresh(GRequest())
    except RefreshError as error:
        raise ReAuthentificationNeededException("token-refresh failed. please re-authenticate.")

def bundleCookie(cookie)->GAPITokenBundle:
    if REFRESH_TOKEN not in cookie:
        raise ReAuthentificationNeededException("refresh token cookie is not found")
    if ACCESS_TOKEN not in cookie:
        raise ReAuthentificationNeededException("access token cookie is not found")
    return GAPITokenBundle(access_token=cookie[ACCESS_TOKEN],refresh_token=cookie[REFRESH_TOKEN])
