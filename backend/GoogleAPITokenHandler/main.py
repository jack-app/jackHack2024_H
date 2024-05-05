from urllib import response
import google.oauth2.credentials
import google_auth_oauthlib.flow
from shared.Units import Sec, MilliSec
from shared.GAPITokenBundle import GAPITokenBundle
import asyncio
import datetime
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
import requests
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
from shared.Exceptions import ReAuthentificationNeededException
from google.auth.exceptions import RefreshError
import secrets

load_dotenv('./GoogleAPITokenHandler/.env')

FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            './GoogleAPITokenHandler/credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )
FLOW.redirect_uri = os.environ['REDIRECT_URI']

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

SIGN_QUEUE = _SignQueue()

class AuthFlowSource:

    def __init__(self):
        self.code = None
        self.state = secrets.token_hex()
        self.result = None

    def sign(state: str, code: str):
        """
        queueにtokenGetterとstateの組が登録されていれば、これにコードをひもづける。
        失敗した場合はValueErrorを返す。
        """
        target = SIGN_QUEUE.get(state)
        if target is None:
            raise ValueError(
                f"designated state: '{state}' is not found in queue: '{AuthFlowSource.states_in_sign_queue.keys()}'"
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
            tokens = FLOW.fetch_token(code=self.code)
            self.result = GAPITokenBundle(
                access_token=tokens["access_token"], 
                refresh_token=tokens["refresh_token"]
            )
        except InvalidGrantError:
            raise ReAuthentificationNeededException("given code was invalid. please re-authenticate.")
        return self.result

    def get_oauth_url(self) -> str:
        authorization_url, state = FLOW.authorization_url(
            accsess_type='offline',
            include_granted_scopes='true',
            approval_prompt='force',
            state=self.state
        )
        SIGN_QUEUE.put(state,self)
        return authorization_url


def construct_cledentials(
    tokenBundle: GAPITokenBundle
):
    return google.oauth2.credentials.Credentials(
        tokenBundle.access_token,
        refresh_token=tokenBundle.refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET']
    )

def revoke_gapi_token(tokenBundle: GAPITokenBundle):
    requests.post('https://oauth2.googleapis.com/revoke',
        params={'token': tokenBundle.access_token},
        headers = {'content-type': 'application/x-www-form-urlencoded'})

def breakdown_cledentials(
    cred: google.oauth2.credentials.Credentials
) -> GAPITokenBundle:
    return GAPITokenBundle(
        access_token=cred.token,
        refresh_token=cred.refresh_token
    )

def refresh_credentials(
    cred: google.oauth2.credentials.Credentials
):
    try:
        cred.refresh(Request())
    except RefreshError as error:
        raise ReAuthentificationNeededException("token-refresh failed. please re-authenticate.")
        

class GoogleApiTokenPopper:
    def __init__(self, tokenBundle: GAPITokenBundle):
        self.cred = construct_cledentials(tokenBundle)
    def pop(self):
        refresh_credentials(self.cred)
        return self.cred.token