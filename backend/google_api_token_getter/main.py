import google.oauth2.credentials
import google_auth_oauthlib.flow
from shared.Units import Sec, MilliSec
from shared.GAPITokenBundle import GAPITokenBundle
import asyncio
import datetime
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request

load_dotenv()

# TODO: sign_queueを定期的に掃除する処理を追加する。5min以上保存している必要はないだろう
class _SignQueue:
    def __init__(self):
        self.records = []
    def put(self, state: str, tokenGetter: str):
        self.records.append((state,tokenGetter,datetime.datetime.now()))
    def popAll(self, state = None, tokenGetter = None):
        response = tuple(record[1] for record in self.records if record[0] == state or record[1] == tokenGetter)
        self.records = [record for record in self.records if record[0] != state and record[1] != tokenGetter]
        return response

class AuthFlowSource:
    sign_queue = _SignQueue()

    def __init__(self):
        self.code = None
        self.result = None
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            './google_api_token_getter/credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )
        self.flow.redirect_uri = os.environ['REDIRECT_URI']

    def __del__(self):
        AuthFlowSource.sign_queue.popAll(tokenGetter=self)

    def sign(state: str, code: str):
        """
        queueにtokenGetterとstateの組が登録されていれば、これにコードをひもづける。
        失敗した場合はValueErrorを返す。
        """
        target = AuthFlowSource.sign_queue.popAll(state=state)[0]
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