from starlette.middleware.cors import CORSMiddleware  # 追加
from shared.Exceptions import ReAuthentificationNeededException
from shared.GAPITokenBundle import GAPITokenBundle
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from shared.AssignmentEntry import AssignmentEntry
from assignmentEntryRegister import assignmentEntryRegister
from GoogleAPITokenHandler.main import AuthFlowSource, breakdown_cledentials, construct_cledentials, refresh_credentials, SIGN_QUEUE

app = FastAPI()

# CORSを回避するために追加（今回の肝）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)


@app.get("/")
def rootRoute(response: Response, request: Request):
    print(response)
    print(request)
    return "You're successfully accessing to the FastAPI server."


@app.post("/register")
async def register_entry(body: AssignmentEntry, request: Request, response: Response):
    # (header)cookieでtokenを受付
    # (body)jsonでassignmentEntryを受付

    # fetch("http://***/register",
    #   {method:"POST",headers: {
    #       'Content-Type': 'application/json',
    #       'sessionToken': 'token'
    #   },
    #   body:JSON.stringify(assignmentEntry)}
    # ) のようにしてリクエストを送ってください。

    try:
        if "refreshToken" not in request.cookies:
            response.status_code = 401
            return {"msg": "refreshToken cookie is not found"}
        if "accessToken" not in request.cookies:
            response.status_code = 401
            return {"msg": "accessToken cookie is not found"}

        token_bandle = GAPITokenBundle(
            access_token=request.cookies["refreshToken"],
            refresh_token=request.cookies["accessToken"]
        )
        cred = construct_cledentials(token_bandle)

        assignmentEntryRegister(body, cred)

        response.status_code = 200
        return {}

    except ReAuthentificationNeededException as e:
        response.status_code = 401
        return {"msg": str(e)}


## GOOGLE TOKEN HANDLER ENDPOINTS ###

@app.get("/refreshTokens")
async def refreshTokens(request: Request, response: Response):

    try:
        if "refreshToken" not in request.cookies:
            response.status_code = 401
            return {"msg": "refreshToken cookie is not found"}
        if "accessToken" not in request.cookies:
            response.status_code = 401
            return {"msg": "accessToken cookie is not found"}

        token_bandle = GAPITokenBundle(
            access_token=request.cookies["refreshToken"],
            refresh_token=request.cookies["accessToken"]
        )
        cred = construct_cledentials(token_bandle)

        refresh_credentials(cred)
        response.status_code = 200

        bundle = breakdown_cledentials(cred)
        response.set_cookie(
            key="refreshToken", value=bundle.refresh_token, httponly=True, secure=True)
        response.set_cookie(
            key="accessToken", value=bundle.access_token, httponly=True, secure=True)

        return {"msg": "successfully done."}

    except ReAuthentificationNeededException as e:
        response.status_code = 401
        return {"msg": str(e)}


@app.get("/getTokens")
async def getTokens(request: Request, response: Response):
    print(request.cookies)
    state = "state unspesified"
    if "AuthFlowState" not in request.cookies:
        response.status_code = 400
        return {"msg": "AuthFlowState cookie is not supplied."}

    state = request.cookies["AuthFlowState"]
    targetFlow = SIGN_QUEUE.get(state)

    try:
        await targetFlow.issue_gapi_tokens()
        SIGN_QUEUE.remove(state)
    except TimeoutError:
        response.status_code = 408
        return {"msg": "getting traial timeout. try again after authorizing this application."}
    except ReAuthentificationNeededException:
        response.status_code = 401
        return {"msg": "code was invaild. try to re-authentificate from scrach."}
    response.set_cookie(
        key="refreshToken", value=targetFlow.result.refresh_token, httponly=True, secure=True)
    response.set_cookie(
        key="accessToken", value=targetFlow.result.access_token, httponly=True, secure=True)

    return {"msg": "successfully done."}


@app.get("/getAuthFlowState")
def issueAuthFlow(response: Response, request: Request):
    authFlow = AuthFlowSource()
    response.set_cookie(key="AuthFlowState",
                        value=authFlow.state, httponly=True, secure=True)

    return {"auth_url": authFlow.get_oauth_url()}


@app.get("/oauth2callback")
async def oauth2callback(state: str, error: None | str = None, code: None | str = None):
    if error:
        return {"msg": error}
    if code is None:
        return {"msg": "code is not found"}
    try:
        AuthFlowSource.sign(state, code)
        html_content = """
        <html>
            <body>
                <script>window.close()</script>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    except Exception as error:
        return {"msg": str(error)}


## GOOGLE TOKEN HANDLER ENDPOINTS ###

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="61000")
