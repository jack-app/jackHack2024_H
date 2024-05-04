from fastapi import Body, FastAPI, Request, Response
from pydantic import BaseModel, Field
from shared.AssignmentEntry import AssignmentEntry
from calenderapiwrapper.main import CalendarAPIWrapper

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
    print(body)


@app.get("/getToken")
async def get_token(response:Response, request:Request):
    # response.set_cookie(key="test", value="test")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="61000")