from datetime import datetime

class AssignmentEntry:
    def __init__(self, course:str , name:str , dueDate:datetime, description:str|None = None):
        self.course = course
        self.name = name
        self.dueDate = dueDate
        self.description = description