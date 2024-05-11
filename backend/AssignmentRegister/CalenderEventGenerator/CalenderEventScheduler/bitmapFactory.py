from ...InterpackageObject.datetime_expansion import timespan
from ...InterpackageObject.dataTransferObject import SleepSchedule
from datetime import time,timedelta,datetime
from .bitmap import FreeBusyBitMap
from ...GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from .config import CELL_INTERVAL
from asyncio import sleep
from math import ceil

async def avoid_task_overlapping(target_timespan: timespan,calender_api_client: GoogleCalenderAPIClient,interval:timedelta=CELL_INTERVAL):
    bitmap = FreeBusyBitMap(scope=target_timespan,interval=interval)
    async for busy_period in calender_api_client.get_busytimes(target_timespan.end):
        bitmap.sign_as_busy_within_scope(busy_period)
    return bitmap

def __cast_time_to_float(time:time):
    """秒以下を無視してfloatに変換する。"""
    return time.hour + time.minute/60 + time.second/3600 + time.microsecond/3600000

def make_margin(bitmap: FreeBusyBitMap, margin: timedelta):
    """
    bitmapのbusyな部分をmarginだけ広げる。
    """
    bitmap = bitmap.clone()

    scope_filter = FreeBusyBitMap(timespan(bitmap.scope.start,bitmap.scope.end),bitmap.interval)
    scope_filter.reverse()
    
    margin_bit_size = ceil(bitmap.interval / margin)
    for i in range(1,margin_bit_size+1):
        bitmap.bitMap |= ( bitmap.bitMap << i)
        bitmap.bitMap |= ( bitmap.bitMap >> i)
    bitmap.bitMap &= scope_filter.bitMap
    return bitmap

async def avoid_sleeping_time(target_timespan: timespan, sleepSchedule: SleepSchedule,interval:timedelta=CELL_INTERVAL):
    """
    睡眠時間をbusyとしてマークする。
    """
    bitmap = FreeBusyBitMap(scope=target_timespan,interval=interval)

    # 活動時間と睡眠時間を取得
    go_to_bed_f = __cast_time_to_float(sleepSchedule.go_to_bed)
    wake_up_f = __cast_time_to_float(sleepSchedule.wake_up)

    sleep_duration = (wake_up_f - go_to_bed_f) % 24

    sleep_duration = timedelta(# ここで秒以下は無視。
        hours=int(sleep_duration),
        minutes=int((sleep_duration % 1)*60) 
    )

    cursor = datetime.combine(
        date=target_timespan.start,
        time=sleepSchedule.go_to_bed,
        tzinfo=target_timespan.start.tzinfo
    ) - timedelta(days=1) #その日の前日の就寝時間に合わせる

    while cursor <= target_timespan.end:
        bitmap.sign_as_busy_within_scope(
            timespan(
                cursor,
                cursor + sleep_duration
            )
        )
        cursor += timedelta(days=1)
        await sleep(0)

    return bitmap