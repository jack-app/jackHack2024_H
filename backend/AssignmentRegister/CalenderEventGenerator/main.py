from ..InterpackageObject.dataTransferObject import Assignment,CalenderEvent,SleepSchedule
from ..InterpackageObject.datetime_expansion import timespan
from ..GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from datetime import datetime,timedelta,timezone,time
from .CalenderEventScheduler import Scheduler

class CalenderEventGenerator:
    def __init__(self,APIClient:GoogleCalenderAPIClient):
        self.google_calender_api_client = APIClient
    async def generate_events(self, assignment:Assignment):
        scheduler = await Scheduler(
            timespan(
                datetime.now(timezone.utc),
                assignment.dueDate
            ),
            self.google_calender_api_client,
            sleepSchedule=SleepSchedule(
                go_to_bed=time(hour=22,minute=0),
                wake_up=time(hour=8,minute=0)
            )
        )
        chunks = await scheduler.get_chunks_fullfill_specs(assignment.duration)
        for chunk in chunks:
            yield CalenderEvent(
                title=assignment.title_of_assignment,
                description=assignment.description,
                start=chunk.start,
                end=chunk.end
            )
