from .config import CELL_INTERVAL,TASK_MARGIN,MINIMUM_CHUNK_SIZE,SUBMISSION_MARGIN
from datetime import timedelta
from ...InterpackageObject.datetime_expansion import timespan
from ...InterpackageObject.dataTransferObject import SleepSchedule
from ...GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from .bitmap import FreeBusyBitMap
from .bitmapFactory import avoid_task_overlapping, avoid_sleeping_time, make_margin
from typing import Any,List,AsyncGenerator,Callable,Coroutine

class Scheduler:
    event_bitmap:FreeBusyBitMap
    sleeping_bitmap:FreeBusyBitMap
    event_bitmap_with_margin:FreeBusyBitMap
    margined_scope:timespan
    interval:timedelta
    minimum_chunk_size:timedelta
    submission_margin:timedelta
    async def __new__(cls, 
        scope: timespan, 
        google_calender_api_client:GoogleCalenderAPIClient, 
        sleepSchedule:SleepSchedule,
        interval:timedelta = CELL_INTERVAL
    ):
        self = super().__new__(cls)
        
        self.margined_scope = timespan(scope.start, scope.end - SUBMISSION_MARGIN)
        self.interval = interval
        self.event_bitmap = await avoid_task_overlapping(scope,google_calender_api_client,interval)
        self.event_bitmap_with_margin = make_margin(self.event_bitmap, TASK_MARGIN)
        self.sleeping_bitmap = await avoid_sleeping_time(scope,sleepSchedule,interval)

        self.minimum_chunk_size = MINIMUM_CHUNK_SIZE
        self.submission_margin = SUBMISSION_MARGIN    

        return self
    
    async def get_free_chunks(self, bitmap:FreeBusyBitMap, required_task_duration:timedelta, minimum_chunk_size:timedelta)->List[timespan]:
        """
        条件(bitmapがfreeを示していること, required_task_duration, minimum_chunk_size)を満たすようなchunkを返す。ただしそのようなchunkのとり方が存在しない場合は空のリストを返す。
        """
        result = []
        current_task_duration = timedelta(0)
        async for chunk in bitmap.get_free_chunks():
            if chunk.duration() >= minimum_chunk_size:
                if current_task_duration + chunk.duration() >= required_task_duration:
                    result.append(
                        timespan(chunk.start, 
                                 max(
                                     chunk.start + required_task_duration - current_task_duration,
                                     chunk.start + minimum_chunk_size
                                 )
                        )
                    )
                    return result
                else:
                    current_task_duration += chunk.duration()
                    result.append(chunk)
        return []

    async def primary_chunk_spec(self, required_duration:timedelta):
        return await self.get_free_chunks(self.event_bitmap_with_margin|self.sleeping_bitmap, required_duration, self.minimum_chunk_size)

    async def secondary_chunk_spec(self, required_duration:timedelta):
        return await self.get_free_chunks(self.event_bitmap, required_duration, self.minimum_chunk_size)

    def last_chunk_spec(self, required_duration:timedelta):
        # margined_scopeの最後までに終わるように。
        return [timespan(self.margined_scope.start + self.margined_scope.duration() - required_duration, self.margined_scope.end)]
    
    async def get_chunks_fullfill_specs(self, required_duration:timedelta):

        specs: List[Callable[[timedelta],Coroutine[Any,Any,List[timespan]]]] = [
            self.primary_chunk_spec,
            self.secondary_chunk_spec,
            self.last_chunk_spec
        ]

        for spec in specs:
            result = await spec(required_duration)
            if result: return result

        