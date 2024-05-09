from ..InterpackageObject.dataTransferObject import Assignment,CalenderEvent
from ..GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from datetime import datetime,timedelta,timezone

class CalenderEventGenerator:
    def __init__(self,APIClient:GoogleCalenderAPIClient):
        self.google_calender_api_client = APIClient
    async def generate(self, assignment:Assignment)->CalenderEvent:
        return CalenderEvent(
            title="mock",
            description="mock",
            start=datetime.now(timezone.utc),
            end=datetime.now(timezone.utc)+timedelta(hours=1),
        )

class AssignmentEvnetConvertor:
    pass
