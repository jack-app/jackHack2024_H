from datetime import datetime

class CalenderEvent:
    def __init__(
            self, 
            title:str, 
            start:datetime, 
            end:datetime,
            description:str|None = None, 
        ):
        self.title = title
        self.description = description

        if start.tzinfo is None:
            raise ValueError(f"timezone is not scepcified in start: {start.isoformat()}")
        if end.tzinfo is None:
            raise ValueError(f"timezone is not scepcified in end: {end.isoformat()}")
        
        self.start = start
        self.end = end
    def __str__(self):
        if self.description:
            return f"{self.title} ({self.description}) from {self.start.isoformat()} to {self.end.isoformat()}"
        return f"{self.title} from {self.start.isoformat()} to {self.end.isoformat()}"