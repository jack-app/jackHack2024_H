import google.oauth2.credentials
import google_auth_oauthlib.flow
from shared.Units import Sec, MilliSec
from shared.GAPITokenBundle import GAPITokenBundle
import asyncio
import datetime

AUTH_FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    './backend/google_api_token_getter/credential.json',
    scopes=['https://www.googleapis.com/auth/calendar.events']
)
AUTH_FLOW.redirect_uri = 'https://jack.hbenpitsu.net/oauth2callback'

class GoogleApiTokenGetter:
    unsinged_states = {}
    signed_states = {}

    def __init__(self):
        self.code = None

    def sing(state: str, code: str):
        """
        stateに対応するcodeを受け取り、stateを削除して、codeをstateに対応するsigned_statesに追加する。
        これに失敗した場合はValueErrorを返す。
        """
        if state in GoogleApiTokenGetter.states_in_sign_queue:
            target = GoogleApiTokenGetter.states_in_sign_queue[state].tokenGetter
            del GoogleApiTokenGetter.states_in_sign_queue[state]
            
            target.code = code

            return
        else:
            raise ValueError(
                f"designated state: '{state}' is not found in queue: '{GoogleApiTokenGetter.states_in_sign_queue.keys()}'"
            )

    async def pop_token(self, timeout: MilliSec = MilliSec(10000), interval: MilliSec = MilliSec(1000)) -> GAPITokenBundle:
        """
        トークンを取得する。
        Timeoutの場合はTimeoutErrorを返す。
        """
        for _ in range(int(timeout / interval) + 1):
            if self.code is not None:
                break
            await asyncio.sleep(interval.toSec())
        
        if self.code is None:
            raise TimeoutError("timeout")
        
        tokens = AUTH_FLOW.fetch_token(code=self.code)

        return GAPITokenBundle(tokens["access_token"], tokens["refresh_token"],tokens["expires_at"] )

    def get_oauth_url(self) -> str:
        authorization_url, state = AUTH_FLOW.authorization_url(
            accsess_type='offline',
            include_granted_scopes='true',
            approval_prompt='force'
        )
        GoogleApiTokenGetter.states_in_sign_queue[state] = _SignQueueEntry(self,datetime.datetime.now())
        return authorization_url

class _SignQueueEntry:
    def __init__(self, tokenGetter: GoogleApiTokenGetter,registerdAt: datetime.datetime):
        self.tokenGetter = tokenGetter
        self.registerdAt = registerdAt

# TODO: states_in_sign_queueを定期的に掃除する処理を追加する。