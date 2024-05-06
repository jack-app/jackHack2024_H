from shared.Exceptions import ReAuthentificationNeededException
from fastapi import FastAPI, Request, Response
from shared.AssignmentEntry import AssignmentEntry
from calenderapiwrapper.assignmentEntryRegister import assignmentEntryRegister
from starlette.middleware.cors import CORSMiddleware
from GAPITokenHandler import GAPITokenHandler

app = FastAPI()

GAPITokenHandler(app)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="61000")