from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Request, Response
from google_auth_oauthlib.flow import Flow
from DEPLOY_SETTING import REDIRECT_URI,CREDENTIAL_FILE_PATH
from GAPITokenHandler.tokenBundle import GAPITokenBundle
from GAPITokenHandler.literals import REFRESH_TOKEN, ACCESS_TOKEN, AUTH_FLOW_STATE
from GAPITokenHandler.exceptions import ReAuthenticationRequired,StateNotExists,TokenNotFound
from GAPITokenHandler.authFlowState import issueStateToQueue, signStateQueue, popCode
from oauthlib.oauth2 import InvalidGrantError

class GAPITokenHandler:
    def __init__(self, app: FastAPI):
        self.APP = app
        self.AUTH_FLOW = Flow.from_client_secrets_file(
            CREDENTIAL_FILE_PATH,
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )
        self.AUTH_FLOW.redirect_uri = REDIRECT_URI
        self.defEndpoints()

    def defEndpoints(self):
        cookie_options = {
            "httponly": True,
            "secure": True
        }

        @self.APP.get("/getAuthFlowState")
        def issueAuthFlow(response:Response, request:Request):    
            url,state = self.AUTH_FLOW.authorization_url(
                accsess_type='offline',
                include_granted_scopes='true',
                approval_prompt='force'
            )
            
            issueStateToQueue(state)
            response.set_cookie(key=AUTH_FLOW_STATE, value=state, **cookie_options)

            return {"auth_url": url, "msg": "success"}

        @self.APP.get("/oauth2callback")
        async def oauth2callback(response:Response, state:str, error: None|str = None, code: None|str = None):
            
            if error:
                response.status_code = 400
                return {"msg":error}
            if code is None:
                response.status_code = 400
                return {"msg":"code is not supplied."}
            
            assert error is None
            assert code is not None

            try:
                signStateQueue(state, code)
            except StateNotExists as e:
                response.status_code = e.http_status
                return {"msg":str(e)}
            
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
                print(state)
                code = await popCode(state)
                tokens = self.AUTH_FLOW.fetch_token(code=code)
            except TimeoutError:
                response.status_code = 408
                return {"msg": "getting traial timeout. try again after authorizing this application."}
            except InvalidGrantError:
                response.status_code = 401
                return {"msg": "code was invaild. try to re-authentificate from scrach."}
            except KeyError:
                response.status_code = 400
                return {"msg": "AuthFlowState cookie is not supplied."} 
            except StateNotExists as e:
                response.status_code = e.http_status
                return {"msg":str(e)}
            
            try:
                response.set_cookie(key=REFRESH_TOKEN,value=tokens[REFRESH_TOKEN], **cookie_options)
                response.set_cookie(key=ACCESS_TOKEN,value=tokens[ACCESS_TOKEN], **cookie_options)
            except:
                response.status_code = 401
                return {"msg": "some tokens are not issued. please re-authenticate."}

            return {"msg": "success"}
    
        @self.APP.get("/refreshTokens")
        async def refreshTokens(request: Request, response: Response):
            try:
                gapibundle = GAPITokenBundle.from_dict(request.cookies)
                gapibundle.refresh()
                response.set_cookie(key=ACCESS_TOKEN,value=gapibundle.access_token, **cookie_options)
                response.set_cookie(key=REFRESH_TOKEN,value=gapibundle.refresh_token, **cookie_options)
                return {"msg": "success"}
            except TokenNotFound as e:
                response.status_code = e.http_status
                return {"msg":str(e)}
            except ReAuthenticationRequired as e:
                response.status_code = e.http_status
                return {"msg":str(e)}


