import google.oauth2.credentials
import google_auth_oauthlib.flow
from shared.Units import Sec, MilliSec
import asyncio
import datetime

AUTH_FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    './credential.json',
    scopes=['https://www.googleapis.com/auth/calendar.events']
)
AUTH_FLOW.redirect_uri = 'https://jack.hbenpitsu.net/authRedirect'

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
        if state in GoogleApiTokenGetter.unsigned_states:
            GoogleApiTokenGetter.signed_states[state] = code
            del GoogleApiTokenGetter.unsigned_states[state]
            
            target.code = code

            return
        else:
            raise ValueError(
                f"designated state: '{state}' is not found in unsigned_states: {GoogleApiTokenGetter.unsigned_states.keys()}"
            )

    async def pop_token(self, timeout: MilliSec = MilliSec(10), interval: MilliSec = MilliSec(1000)) -> str:
        """トークンを取得する。"""
        for _ in range(int(timeout / interval) + 1):
            if self.code is not None:
                break
            await asyncio.sleep(interval.toSec())


    def get_oauth_url(self) -> str:
        authorization_url, state = AUTH_FLOW.authorization_url(
            accsess_type='offline',
            include_granted_scopes='true'
        )
        GoogleApiTokenGetter.sessionToken_stateMap[state] = _SignQueueEntry(self,datetime.datetime.now())
        return authorization_url

class _SignQueueEntry:
    def __init__(self, tokenGetter: GoogleApiTokenGetter,registerdAt: datetime.datetime):
        self.tokenGetter = tokenGetter
        self.registerdAt = registerdAt

# TODO: states_in_sign_queueを定期的に掃除する処理を追加する。