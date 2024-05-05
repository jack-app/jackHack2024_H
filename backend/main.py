from fastapi import FastAPI, Request, Response
from shared.AssignmentEntry import AssignmentEntry
from assignmentEntryRegister import assignmentEntryRegister
from sessionmanager.main import SessionManager
from google_api_token_getter.main import AuthFlowSource

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
        if "sessionToken" not in request.cookies:
            response.status_code = 401
            response.body = {
                "msg":"sessionToken is not found"
            }
            return
        assignmentEntryRegister(body,request.cookies["sessionToken"])
        response.status_code = 200
        response.body = {}
    except Exception as error:
        response.status_code = 500
        response.body = {
            "msg":str(error)
        }


@app.get("/getToken")
async def get_token(response:Response, request:Request):
    sessionManager = SessionManager()
    response.status_code = 200
    response.set_cookie(key="sessionToken", value=sessionManager.getSessionToken(),secure=True)
    # response.body = {
    #     "auth_url": sessionManager.getAuthURL()
    # }
    return response

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