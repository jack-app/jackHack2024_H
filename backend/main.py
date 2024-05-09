from fastapi import Request, Response
from shared.AssignmentEntry import AssignmentEntry
# from calenderapiwrapper.assignmentEntryRegister import assignmentEntryRegister
from AuthHandler import GoogleAPITokenHandler
from server import Server

serv = Server()
GoogleAPITokenHandler(serv.APP)

app = serv.APP

# from AuthHandler.GoogleAPITokenHandler import GoogleAPITokenBundle
# from AuthHandler.GoogleAPITokenHandler.exceptions import TokenNotFound, ReAuthenticationRequired
# @app.post("/register")
# async def register_entry(body:AssignmentEntry,request:Request,response:Response):
#     # (header)cookieでtokenを受付
#     # (body)jsonでassignmentEntryを受付
    
#     # fetch("http://***/register",
#     #   {method:"POST",headers: {
#     #       'Content-Type': 'application/json'
#     #   },
#     #   body:JSON.stringify(assignmentEntry)}
#     # ) のようにしてリクエストを送ってください。

#     try:
#         bundle = GoogleAPITokenBundle.from_dict(request.cookies)        
#         assignmentEntryRegister(body,bundle.asCredentials())
#         return {"msg":"success"}
#     except TokenNotFound as e:
#         response.status_code = 400
#         return {"msg":str(e)}
#     except ReAuthenticationRequired as e:
#         response.status_code = 401
#         return {"msg":str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="8000")