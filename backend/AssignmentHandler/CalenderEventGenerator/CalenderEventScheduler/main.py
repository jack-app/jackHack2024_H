from .config import CELL_INTERVAL
from datetime import timedelta
from ...InterpackageObject.datetime_expansion import timespan
from ...InterpackageObject.dataTransferObject import SleepSchedule
from ...GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from .util import FreeBusyBitMap
from .bitmapFactory import avoid_task_overlapping, avoid_sleeping_time

class Scheduler:
    event_bitmap:FreeBusyBitMap
    sleeping_bitmap:FreeBusyBitMap
    scope:timespan
    margin:timedelta
    async def __new__(cls, 
        scope: timespan, 
        google_calender_api_client:GoogleCalenderAPIClient, 
        sleepSchedule:SleepSchedule,
        interval:timedelta = CELL_INTERVAL
    ):
        self = super().__new__(cls)
        
        self.scope = scope
        self.event_bitmap = await avoid_task_overlapping(scope,google_calender_api_client,interval)
        self.sleeping_bitmap = await avoid_sleeping_time(scope,sleepSchedule,interval)

        return self
    
    async def get_primal_free_chunks(self, length:timedelta):
        async for chunk in (self.event_bitmap | self.sleeping_bitmap).get_free_timespans():
            if chunk.duration >= length:
                yield chunk
    
    async def get_secondal_free_chunks(self, length:timedelta):
        async for chunk in (self.event_bitmap).get_free_timespans():
            if chunk.duration >= length:
                yield chunk
    
    def last_candidate(self, length:timedelta):
        # scopeの最後にちょうど終わるように。
        return timespan(self.scope.start + self.scope.duration - length, self.scope.end)
    
    async def get_some_chunk(self, length:timedelta):
        async for chunk in self.get_primal_free_chunks(length):
            return chunk
        async for chunk in self.get_secondal_free_chunks(length):
            return chunk
        return self.last_candidate(length)
        
        
        