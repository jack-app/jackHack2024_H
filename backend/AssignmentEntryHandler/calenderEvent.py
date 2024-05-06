from datetime import datetime

class CalenderEvent:
    def __init__(
            self, 
            title:str, 
            description:str, 
            start:datetime, 
            end:datetime
        ):
        self.title = title
        self.description = description
        self.start = start
        self.end = end