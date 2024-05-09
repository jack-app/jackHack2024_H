from fastapi import FastAPI,Request,Response
from pydantic import BaseModel
from .InterpackageObject.dataTransferObject import Assignment
from .CalenderEventGenerator import CalenderEventGenerator
from .CalenderEventRegister import CalenderEventRegister
from datetime import datetime,timedelta
from .exceptions import ReAuthorizationRequired
from AuthHandler import GoogleAPITokenBundle
from AuthHandler.GoogleAPITokenHandler.exceptions import TokenNotFound
from .GoogleCalenderAPIWrapper import GoogleCalenderAPIClient

class AssignmentHandler:
    def __init__(self, app:FastAPI = FastAPI()):
        self.APP = app
        self.defEndpoints()

    class __assignmentRegisterCommand(BaseModel):
        course_name:str
        title_of_assignment:str
        dueDate:datetime
        duration:timedelta
        description:str|None = None

    def defEndpoints(self):
        
        @self.APP.post("/register")
        async def registerAssignmentEntry(request:Request,response:Response,command:self.__assignmentRegisterCommand):
            assignment = Assignment(
                course_name=command.course_name,
                title_of_assignment=command.title_of_assignment,
                dueDate=command.dueDate,
                duration=command.duration,
                description=command.description
            )
            try:
                tokenBundle = GoogleAPITokenBundle.from_dict(request.cookies)
                GoogleAPI_client = GoogleCalenderAPIClient(tokenBundle)

                calender_event = await CalenderEventGenerator(GoogleAPI_client).generate(assignment)
                event_id = await CalenderEventRegister(GoogleAPI_client).register(calender_event)
                return {"msg":"success","event_id":event_id}

            except ReAuthorizationRequired as e:
                response.status_code=e.http_status
                return {"msg":str(e)}
            except TokenNotFound as e:
                response.status_code=e.http_status
                return {"msg":str(e)}

            