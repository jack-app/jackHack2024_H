from fastapi import FastAPI, Request, Response
from calenderapiwrapper.main import CalendarAPIWrapper

app = FastAPI()

@app.get("/")
def rootRoute(response:Response, request:Request):
    print(response)
    print(request)
    return "You're successfully accessing to the FastAPI server."

@app.get("/register/")
def register_entry(response:Response, request:Request):
    # (header)cookieでsessionTokenを受付
    # (body)jsonでassignmentEntryを受付
    response.status_code = 200
    # sessionToken = request.headers[""]
    print(request.headers)
    assignmentEntry = request.body
    return response

@app.get("/getToken/")
def get_token(response:Response, request:Request):
    # response.set_cookie(key="test", value="test")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="61000")