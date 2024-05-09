from fastapi import FastAPI
from pydantic import BaseModel
from .InterpackageObject.dataTransferObject import Assignment

class assignmentHandler:
    def __init__(self, app:FastAPI = FastAPI()):
        self.APP = app

    class __assignmentRegisterCommand(BaseModel):
        course:str
        name:str
        dueDate:str
        duration:str
        description:str|None = None

    def defEndpoint(self):
        
        @self.APP.post("/registerAssignmentEntry")
        async def registerAssignmentEntry(command:self.__assignmentRegisterCommand):
            assignment = Assignment(
                course=command.course,
                name=command.name,
                dueDate=command.dueDate,
                duration=command.duration,
                description=command.description
            )
            