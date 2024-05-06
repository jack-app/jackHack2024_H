from shared.Exceptions import ReAuthentificationNeededException
from fastapi import FastAPI, Request, Response
from shared.AssignmentEntry import AssignmentEntry
from calenderapiwrapper.assignmentEntryRegister import assignmentEntryRegister
from GoogleAPITokenHandler.main import *
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://accounts.google.com/*",
        "https://tact.ac.thers.ac.jp/*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def rootRoute(request:Request,response:Response):
    return "You're successfully accessing to the FastAPI server."

@app.post("/register")
async def register_entry(body:AssignmentEntry,request:Request,response:Response):
    # (header)cookieでtokenを受付
    # (body)jsonでassignmentEntryを受付
    
    # fetch("http://***/register",
    #   {method:"POST",headers: {
    #       'Content-Type': 'application/json'
    #   },
    #   body:JSON.stringify(assignmentEntry)}
    # ) のようにしてリクエストを送ってください。

    try:
        token_bandle = bundleCookie(request.cookies)        
        cred = construct_cledentials(token_bandle)
        assignmentEntryRegister(body,cred)
        return {"msg":"success"}
    except ReAuthentificationNeededException as e:
        response.status_code = 401
        return {"msg":str(e)}


## GOOGLE TOKEN HANDLER ENDPOINTS ###

@app.get("/refreshTokens")
async def refreshTokens(request: Request, response: Response):

    try:
        token_bandle = bundleCookie(request.cookies)
        cred = construct_cledentials(token_bandle)
        refresh(cred)
        response.set_cookie(key=REFRESH_TOKEN,value=cred.refresh_token,httponly=True,secure=True)
        response.set_cookie(key=ACCESS_TOKEN,value=cred.token,httponly=True,secure=True)
        return {"msg": "success"}
    except ReAuthentificationNeededException as e:
        response.status_code = 401
        return {"msg":str(e)}

@app.get("/getTokens")
async def getTokens(request: Request, response: Response):
    state = "state unspesified"
    if AUTH_FLOW_STATE not in request.cookies:
        response.status_code = 400
        return {"msg": "AuthFlowState cookie is not supplied."}
    state = request.cookies[AUTH_FLOW_STATE]
    try:
        targetFlow = AuthFlowSource.SIGN_QUEUE.get(state)
        await targetFlow.issue_gapi_tokens()
        AuthFlowSource.SIGN_QUEUE.remove(state)
    except TimeoutError:
        response.status_code = 408
        return {"msg": "getting traial timeout. try again after authorizing this application."}
    except ReAuthentificationNeededException:
        response.status_code = 401
        return {"msg": "code was invaild. try to re-authentificate from scrach."}
    except KeyError:
        response.status_code = 400
        return {"msg": "state is not found."}
    
    response.set_cookie(key=REFRESH_TOKEN,value=targetFlow.result.refresh_token,httponly=True,secure=True)
    response.set_cookie(key=ACCESS_TOKEN,value=targetFlow.result.access_token,httponly=True,secure=True)
    
    return {"msg": "success"}


@app.get("/getAuthFlowState")
def issueAuthFlow(response:Response, request:Request):
    
    authFlow = AuthFlowSource()
    response.set_cookie(key=AUTH_FLOW_STATE, value=authFlow.state ,httponly=True ,secure=True)
    
    return {"auth_url": authFlow.get_oauth_url()}

@app.get("/oauth2callback")
async def oauth2callback(response:Response, state:str, error: None|str = None, code: None|str = None):
    if error:
        response.status_code = 400
        return {"msg":error}
    if code is None:
        response.status_code = 400
        return {"msg":"code is not found"}
    try:
        AuthFlowSource.sign(state, code)
    except Exception as error:
        response.status_code = 500
        return {"msg":str(error)}
    
    html_content = """
    <html>
        <body>
            <script>window.close()</script>
            <h1>このウィンドウは閉じて構いません。</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

## GOOGLE TOKEN HANDLER ENDPOINTS ###

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="61000")