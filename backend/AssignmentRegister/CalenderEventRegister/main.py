from ..GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from ..InterpackageObject.dataTransferObject import CalenderEvent
from AuthHandler import GoogleAPITokenBundle

class CalenderEventRegister: 
    def __init__(self,APIClient:GoogleCalenderAPIClient):
        self.google_calender_api_client = APIClient
    async def register(self, event: CalenderEvent):
       """event_idを返します。"""
       return await self.google_calender_api_client.register_event(event)