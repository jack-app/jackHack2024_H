from pkg_resources import require
from backend.shared.Exceptions import ReAuthentificationNeededException
from backend.shared.GAPITokenBundle import GAPITokenBundle
from fastapi import FastAPI, Request, Response
from shared.AssignmentEntry import AssignmentEntry
from assignmentEntryRegister import assignmentEntryRegister
from sessionmanager.main import SessionManager
from GoogleAPITokenHandler.main import AuthFlowSource, construct_cledentials

app = FastAPI()


@app.get("/")
def rootRoute(response:Response, request:Request):
    print(response)
    print(request)
    return "You're successfully accessing to the FastAPI server."

@app.post("/register")
async def register_entry(body: AssignmentEntry,response:Response, request:Request):
    # (header)cookieでsessionTokenを受付
    # (body)jsonでassignmentEntryを受付
    
    # fetch("http://127.0.0.1:61000/bodyGetTest",
    #   {method:"POST",headers: {
    #       'Content-Type': 'application/json',
    #       'sessionToken': 'token'
    #   },
    #   body:JSON.stringify(assignmentEntry)}
    # ) のようにしてリクエストを送ってください。

    try:
        if "refreshToken" not in request.cookies:
            response.status_code = 401
            return {"msg":"refreshToken cookie is not found"}
        if "accessToken" not in request.cookies:
            response.status_code = 401
            return {"msg":"accessToken cookie is not found"}
        
        token_bandle = GAPITokenBundle(
            access_token=request.cookies["refreshToken"],
            refresh_token=request.cookies["accessToken"]
        )
        cred = construct_cledentials(token_bandle)
        assignmentEntryRegister(body,cred)
        response.status_code = 200
        return {}
    except ReAuthentificationNeededException as e:
        response.status_code = 401
        return {"msg":str(e)}

@app.get("/getTokens")
async def getToken(request: Request, response: Response):
    if "AuthFlowState" in request.cookies:
        state = request.cookies["AuthFlowState"]
        response.status_code = 400
        return {"msg": "AuthFlowState cookie is not supplied."}
    
    targetFlow = AuthFlowSource.queue.get(state)
    
    try:
        await targetFlow.issue_gapi_tokens()
        AuthFlowSource.queue.remove(state)
    except TimeoutError:
        response.status_code = 408
        return {"msg": "getting traial timeout. try again after authorizing this application."}
    except ReAuthentificationNeededException:
        response.status_code = 401
        return {"msg": "code was invaild. try to re-authentificate from scrach."}
    response.set_cookie(key="refreshToken",value=targetFlow.result.refresh_token,httponly=True,secure=True)
    response.set_cookie(key="accessToken",value=targetFlow.result.access_token,httponly=True,secure=True)
    
    return {"msg": "successfully done."}

@app.get("/getAuthFlowState")
def issueAuthFlow(response:Response, request:Request):
    authFlow = AuthFlowSource()
    response.set_cookie(key="AuthFlowState", value=authFlow.state ,secure=True)
    
    return {"auth_url": authFlow.get_oauth_url()}

@app.get("/oauth2callback")
async def oauth2callback(state: str, error: None|str = None, code: None|str = None):
    if error:
        return {"msg":error}
    if code is None:
        return {"msg":"code is not found"}
    try:
        AuthFlowSource.sign(state, code)
        return {"msg":"success"}
    except Exception as error:
        return {"msg":"internal server error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="61000")