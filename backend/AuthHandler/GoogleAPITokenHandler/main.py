from fastapi import FastAPI,HTTPException,Request, Response
from fastapi.responses import HTMLResponse
from google_auth_oauthlib.flow import Flow
from DEPLOY_SETTING import REDIRECT_URI,CREDENTIAL_FILE_PATH
from .tokenBundle import GoogleAPITokenBundle
from .literals import REFRESH_TOKEN, ACCESS_TOKEN, AUTH_FLOW_STATE
from .exceptions import ReAuthenticationRequired,TokenNotFound
from ..SignQueue.exceptions import StateNotExists
from ..SignQueue import SignQueue
from oauthlib.oauth2 import InvalidGrantError

class GoogleAPITokenHandler:
    def __init__(self, app: FastAPI):
        self.APP = app
        self.AUTH_FLOW = Flow.from_client_secrets_file(
            CREDENTIAL_FILE_PATH,
            scopes=['https://www.googleapis.com/auth/calendar.events',
                    'https://www.googleapis.com/auth/calendar.readonly',]
        )
        self.AUTH_FLOW.redirect_uri = REDIRECT_URI
        self.sign_queue = SignQueue()
        self.defEndpoints()

    def get_auth_url(self):
        url,state = self.AUTH_FLOW.authorization_url(
            accsess_type='offline',
            include_granted_scopes='true',
            approval_prompt='force'
        )
        return url,state

    def defEndpoints(self):
        cookie_options = {
            "httponly": True,
            "secure": True
        }

        @self.APP.get("/getAuthFlowState")
        def issueAuthFlow(response:Response):    
            url,state = self.get_auth_url()
            self.sign_queue.issueState(state)
            response.set_cookie(key=AUTH_FLOW_STATE, value=state, **cookie_options)
            return {"auth_url": url, "detail": "success"}

        @self.APP.get("/oauth2callback")
        async def oauth2callback(state:str, error: None|str = None, code: None|str = None):
            
            if error:
                raise HTTPException(status_code=400, detail=error)
            if code is None:
                raise HTTPException(status_code=400, detail="code is not supplied.")
            
            assert error is None
            assert code is not None

            self.sign_queue.sign(state, code)
            
            html_content = """
            <html>
                <body>
                    <script>window.close()</script>
                    <h1>このウィンドウは閉じて構いません。</h1>
                </body>
            </html>
            """
            return HTMLResponse(content=html_content)
        
        @self.APP.get("/getTokens")
        async def getTokens(request: Request, response: Response):
            
            try:
                state = request.cookies[AUTH_FLOW_STATE]
            except KeyError:
                raise HTTPException(status_code=400, detail="AuthFlowState cookie is not supplied.")
            
            code = await self.sign_queue.pop(state)

            # https://developers.google.com/identity/protocols/oauth2/web-server?hl=ja#exchange-authorization-code
            try:
                tokens = self.AUTH_FLOW.fetch_token(code=code)
            except InvalidGrantError:
                raise HTTPException(status_code=401, detail="code was invaild. try to re-authentificate from scrach.")
            
            try:
                response.set_cookie(key=REFRESH_TOKEN,value=tokens[REFRESH_TOKEN], **cookie_options)
                response.set_cookie(key=ACCESS_TOKEN,value=tokens[ACCESS_TOKEN], **cookie_options)
            except KeyError:
                raise HTTPException(status_code=401, detail="tokens are not issued. re-authenticate.")

            return {"detail": "success"}
    
        @self.APP.get("/refreshTokens")
        async def refreshTokens(request: Request, response: Response):
            gapibundle = GoogleAPITokenBundle.from_dict(request.cookies)
            await gapibundle.refresh()
            response.set_cookie(key=ACCESS_TOKEN,value=gapibundle.access_token, **cookie_options)
            response.set_cookie(key=REFRESH_TOKEN,value=gapibundle.refresh_token, **cookie_options)
            return {"detail": "success"}

    
        @self.APP.get("/revokeTokens")
        async def revokeTokens(request: Request, response: Response):
            gapibundle = GoogleAPITokenBundle.from_dict(request.cookies)
            await gapibundle.revoke()
            response.delete_cookie(key=ACCESS_TOKEN, **cookie_options)
            response.delete_cookie(key=REFRESH_TOKEN, **cookie_options)
            return {"detail": "success"}
