from .config import CELL_INTERVAL
from datetime import timedelta
from ...InterpackageObject.datetime_expansion import timespan
from ...InterpackageObject.dataTransferObject import SleepSchedule
from ...GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from .util import FreeBusyBitMap
from .bitmapFactory import avoid_task_overlapping, avoid_sleeping_time, make_margin

class Scheduler:
    event_bitmap:FreeBusyBitMap
    sleeping_bitmap:FreeBusyBitMap
    event_bitmap_with_margin:FreeBusyBitMap
    scope:timespan
    interval:timedelta
    margin:timedelta
    async def __new__(cls, 
        scope: timespan, 
        google_calender_api_client:GoogleCalenderAPIClient, 
        sleepSchedule:SleepSchedule,
        interval:timedelta = CELL_INTERVAL
    ):
        self = super().__new__(cls)
        
        self.scope = scope
        self.interval = interval
        self.event_bitmap = await avoid_task_overlapping(scope,google_calender_api_client,interval)
        self.event_bitmap_with_margin = make_margin(self.event_bitmap, timedelta(minutes=15))
        self.sleeping_bitmap = await avoid_sleeping_time(scope,sleepSchedule,interval)

        return self
    
    async def get_primal_free_chunks(self, minimum_size:timedelta):
        async for chunk in (self.event_bitmap_with_margin | self.sleeping_bitmap).get_free_timespans():
            if chunk.duration >= minimum_size:
                yield chunk
    
    async def get_secondal_free_chunks(self, minimum_size:timedelta):
        async for chunk in (self.event_bitmap).get_free_timespans():
            if chunk.duration >= minimum_size:
                yield chunk
    
    def last_candidate(self, length:timedelta):
        # scopeの最後にちょうど終わるように。
        return timespan(self.scope.start + self.scope.duration - length, self.scope.end)
    
    async def __get_discret_chanks(self, required_durarion:timedelta, minimum_chunk_size:timedelta = timedelta(minutes=15)):
        current_duration = timedelta(0)
        selected_period_map = FreeBusyBitMap(scope=self.scope,interval=self.interval)
        async for chunk in self.get_primal_free_chunks(minimum_chunk_size):
            if current_duration + chunk.duration() >= required_durarion:
                selected_period_map.sign_as_busy(chunk)
                return timespan(chunk.start, chunk.start + (required_durarion - current_duration))
            else:
                yield chunk
                current_duration += chunk.duration()

    async def get_joined_chanks(self, required_durarion:timedelta, minimum_chunk_size:timedelta = timedelta(minutes=15)):
        async for chunk in self.__get_discret_chanks(required_durarion, minimum_chunk_size):
            yield chunk

#######WIP!########
            
        