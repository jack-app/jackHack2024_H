from AssignmentRegister.CalenderEventGenerator.CalenderEventScheduler import bitmapFactory
from AssignmentRegister.CalenderEventGenerator.CalenderEventScheduler.bitmap import FreeBusyBitMap
from asyncio import run
from AssignmentRegister.InterpackageObject.datetime_expansion import timespan
from AssignmentRegister.InterpackageObject.dataTransferObject import SleepSchedule
from datetime import datetime,time,timezone,timedelta

async def test(fr:datetime):
    target_timespan = timespan(fr,fr+timedelta(days=7))
    # bitmap = await bitmapFactory.avoid_task_overlapping(target_timespan,calender_api_client)
    bitmap = await bitmapFactory.avoid_sleeping_time(target_timespan, 
        SleepSchedule(
            go_to_bed=time(hour=20, minute=30), 
            wake_up=time(hour=5, minute=30)
        )
    )
    print(bitmap)

for d in range(24):
    fr = datetime.now(timezone.utc).replace(hour=d,minute=0,second=0,microsecond=0)
    run(test(fr))
    
bitmap = FreeBusyBitMap(scope=timespan(start=datetime.now(timezone.utc),end=datetime.now(timezone.utc)+timedelta(days=7)), interval=timedelta(minutes=30))
bitmap._sign_as_busy(timespan(start=datetime.now(timezone.utc)+timedelta(days=2),end=datetime.now(timezone.utc)+timedelta(days=3)))
print(bitmap)
print(bitmapFactory.make_margin(bitmap, timedelta(hours=2)))