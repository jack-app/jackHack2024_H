from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from shared.AssignmentEntry import AssignmentEntry
from calenderapiwrapper.main import CalendarAPIWrapper

app = FastAPI()

from pydantic import BaseModel
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get("/")
def rootRoute(response:Response, request:Request):
    print(response)
    print(request)
    return "You're successfully accessing to the FastAPI server."

from typing import Union
class TestBody(BaseModel):
    test: Union [str , None] = None
@app.post("/register/")
def register_entry(body: TestBody ): #,response:Response, request:Request
    # (header)cookieでsessionTokenを受付
    # (body)jsonでassignmentEntryを受付
    print(body)

    # response.status_code = 200
    # # sessionToken = request.headers[""]
    # print(request.headers)
    # assignmentEntry = request.body
    # return response
    # print(request.body())
    # response.status_code = 200
    # response.body = {}
    # return response

@app.get("/getToken/")
def get_token(response:Response, request:Request):
    # response.set_cookie(key="test", value="test")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="61000")