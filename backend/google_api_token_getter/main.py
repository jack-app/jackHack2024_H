import google.oauth2.credentials
import google_auth_oauthlib.flow
from shared.Units import Sec, MilliSec
from shared.GAPITokenBundle import GAPITokenBundle
import asyncio
import datetime
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from typing import Callable

load_dotenv()

class _SignQueue:
    def __init__(self, authFlow_abandoned_by = datetime.timedelta(minutes=5)):
        self.records = {}
        self.authFlow_abandoned_by = authFlow_abandoned_by
    def put(self, state: str, authFlow: str):
        self.records[state]= (authFlow,datetime.datetime.now())

        if len(self.records) > 50:
            asyncio.create_task(self.clean_up())
        
    def pop(self, state):
        response = self.records[state][0]
        del self.records[state]
        return response
    async def clean_up(self):
        for key in self.records.keys():
            try:
                if datetime.datetime.now() - self.records[key][1] > self.authFlow_abandoned_by:
                    del self.records[key]
                await asyncio.sleep(0.1)
            except KeyError:
                pass
class AuthFlowSource:
    sign_queue = _SignQueue()

    def __init__(self, callback_function_on_signed: Callable[[GAPITokenBundle], None]):
        self.code = None
        self.result = None
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            './google_api_token_getter/credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )
        self.flow.redirect_uri = os.environ['REDIRECT_URI']

    def sign(state: str, code: str):
        """
        queueにtokenGetterとstateの組が登録されていれば、これにコードをひもづける。
        失敗した場合はValueErrorを返す。
        """
        target = AuthFlowSource.sign_queue.pop(state=state)[0]
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
        
        tokens = self.flow.fetch_token(code=self.code)
        self.result = GAPITokenBundle(tokens["access_token"], tokens["refresh_token"])
        
        return self.result

    def get_credentials(self, timeout: MilliSec = MilliSec(10000), interval: MilliSec = MilliSec(1000)) -> google.oauth2.credentials.Credentials:
        if not self.flow.credentials:
            self.issue_gapi_tokens(timeout, interval)
        return self.flow.credentials

    def get_oauth_url(self) -> str:
        authorization_url, state = self.flow.authorization_url(
            accsess_type='offline',
            include_granted_scopes='true',
            approval_prompt='force'
        )
        AuthFlowSource.sign_queue.put(state,self)
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

class GoogleApiTokenPopper:
    def __init__(self, tokenBundle: GAPITokenBundle):
        self.cred = construct_cledentials(tokenBundle)
    def pop(self):
        self.cred.refresh(Request())
        return self.cred.token