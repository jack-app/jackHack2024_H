from datetime import datetime,timedelta
from pydantic import BaseModel,model_validator

class Assignment(BaseModel):
    course:str
    name:str
    dueDate:datetime
    duration:timedelta|None
    description:str|None

class assignmentRegisterCommand(BaseModel):
    assingment: Assignment

class CalenderEvent(BaseModel):
    title:str
    description:str|None
    start:datetime
    end:datetime

    @model_validator(mode='after')
    def validate_start_end(self):
        if self.start.tzinfo is None:
            raise ValueError(f"timezone is not scepcified in start: {self.start.isoformat()}")
        if self.end.tzinfo is None:
            raise ValueError(f"timezone is not scepcified in end: {self.end.isoformat()}")
        if self.start > self.end:
            raise ValueError(f"start is later than end: {self.start.isoformat()} > {self.end.isoformat()}")
        return self
    
    def __str__(self):
        if self.description:
            return f"{self.title} ({self.description}) from {self.start.isoformat()} to {self.end.isoformat()}"
        return f"{self.title} from {self.start.isoformat()} to {self.end.isoformat()}"