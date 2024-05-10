from AssignmentRegister.CalenderEventGenerator.CalenderEventScheduler import bitmapFactory
from asyncio import run
from AssignmentRegister.InterpackageObject.datetime_expansion import timespan
from datetime import datetime,time,timezone,timedelta

async def test(fr:datetime):
    target_timespan = timespan(fr,fr+timedelta(days=7))
    # bitmap = await bitmapFactory.avoid_task_overlapping(target_timespan,calender_api_client)
    bitmap = await bitmapFactory.avoid_sleeping_time(target_timespan, time(hour=20, minute=30), time(hour=5, minute=30))
    print(bitmap)

for d in range(24):
    fr = datetime.now(timezone.utc).replace(hour=d,minute=0,second=0,microsecond=0)
    run(test(fr))
