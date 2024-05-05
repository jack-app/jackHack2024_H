from shared.Exceptions import ReAuthentificationNeededException
from fastapi import FastAPI, Request, Response
from shared.AssignmentEntry import AssignmentEntry
from calenderapiwrapper.assignmentEntryRegister import assignmentEntryRegister
from GoogleAPITokenHandler.main import *
from shared.Exceptions import ReAuthentificationNeededException
from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()

from starlette.middleware.cors import CORSMiddleware
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
        tokensExist(request.cookies,response)
        cred = construct_cledentials(request.cookies[ACCESS_TOKEN],request.cookies[REFRESH_TOKEN])
        assignmentEntryRegister(body,cred)
        return {"msg":"success"}
    except ReAuthentificationNeededException as e:
        response.status_code = 401
        return {"msg":str(e)}


## GOOGLE TOKEN HANDLER ENDPOINTS ###

@app.get("/refreshTokens")
async def refreshTokens(request: Request, response: Response):

    try:
        tokensExist(request.cookies,response)
        cred = construct_cledentials(request.cookies[ACCESS_TOKEN],request.cookies[REFRESH_TOKEN])
        refresh(cred)
        response.set_cookie(key=REFRESH_TOKEN,value=cred.refresh_token,httponly=True,secure=True)
        response.set_cookie(key=ACCESS_TOKEN,value=cred.token,httponly=True,secure=True)
        return {"msg": "success"}
    except ReAuthentificationNeededException as e:
        response.status_code = 401
        return {"msg":str(e)}

@app.get("/redirectToAuthURL")
def redirectToAuthURL(response:Response):
    authorization_url, _ = AUTH_FLOW.authorization_url(
        accsess_type='offline',
        include_granted_scopes='true',
        approval_prompt='force',
    )
    return RedirectResponse(authorization_url)

@app.get("/oauth2callback")
async def oauth2callback(response:Response, error: None|str = None, code: None|str = None):
    if error:
        response.status_code = 400
        return {"msg":error}
    if code is None:
        response.status_code = 400
        return {"msg":"code is not found"}
    try:
        tokens = AUTH_FLOW.fetch_token(code=code)
    except Exception as error:
        response.status_code = 500
        return {"msg":str(error)}
    response.set_cookie(key=REFRESH_TOKEN,value=tokens[REFRESH_TOKEN],httponly=True,secure=True)
    response.set_cookie(key=ACCESS_TOKEN,value=tokens[ACCESS_TOKEN],httponly=True,secure=True)
    
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