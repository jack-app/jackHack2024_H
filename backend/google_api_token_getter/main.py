import google.oauth2.credentials
import google_auth_oauthlib.flow

_auth_flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    './credential.json',
    scopes=['https://www.googleapis.com/auth/calendar.events']
)
_auth_flow.redirect_uri = 'https://jack.hbenpitsu.net/authRedirect'

class GoogleApiTokenGetter:
    unsinged_states = {}
    signed_states = {}

    def sing(state: str, code: str):
        """
        stateに対応するcodeを受け取り、stateを削除して、codeをstateに対応するsigned_statesに追加する。
        これに失敗した場合はValueErrorを返す。
        """
        if state in GoogleApiTokenGetter.unsigned_states:
            GoogleApiTokenGetter.signed_states[state] = code
            del GoogleApiTokenGetter.unsigned_states[state]
            return
        else:
            raise ValueError(
                f"designated state: '{state}' is not found in unsigned_states: {GoogleApiTokenGetter.unsigned_states.keys()}"
            )

    # async def pop_token(self, timeout) -> str:

    def get_oauth_url(self) -> str:
        authorization_url, state = self.auth_flow.authorization_url(
            accsess_type='offline',
            include_granted_scopes='true'
        )
        GoogleApiTokenGetter.sessionToken_stateMap[state] = self
        return authorization_url
