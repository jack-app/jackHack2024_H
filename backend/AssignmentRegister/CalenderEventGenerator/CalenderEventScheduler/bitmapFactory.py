from ...InterpackageObject.datetime_expansion import timespan
from ...InterpackageObject.dataTransferObject import SleepSchedule
from datetime import time,timedelta,datetime
from .util import FreeBusyBitMap
from ...GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from .config import CELL_INTERVAL
from asyncio import sleep
from math import ceil

async def avoid_task_overlapping(target_timespan: timespan,calender_api_client: GoogleCalenderAPIClient,interval:timedelta=CELL_INTERVAL):
    bitmap = FreeBusyBitMap(scope=target_timespan,interval=interval)
    async for busy_period in calender_api_client.get_busytimes(target_timespan.end):
        bitmap.sign_as_busy(busy_period)
    return bitmap

def __cast_time_to_float(time:time):
    return time.hour + time.minute/60 + time.second/3600 + time.microsecond/3600000

def make_margin(bitmap: FreeBusyBitMap, margin: timedelta):
    """
    bitmapのbusyな部分をmarginだけ広げる。
    """
    bitmap = bitmap.clone()
    margin_bit_size = ceil(bitmap.interval / margin)
    for i in range(1,margin_bit_size+1):
        bitmap.bitMap |= ( bitmap.bitMap << i)
        bitmap.bitMap |= ( bitmap.bitMap >> i)
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

    # 続く2ブロックの処理は似通っているが、それぞれの処理が必要である。

    # target_timespanのstartが起床時間前だったら起床時間までマークする。
    first_wake_up = datetime.combine(
        date=target_timespan.start,
        time=sleepSchedule.wake_up,
        tzinfo=target_timespan.start.tzinfo
    )
    # 0時スタート、5時起床の場合True
    # 23時スタート、5時起床の場合False
    # first_wake_upがスタートした日付における起床時間を取るためである。
    # つまり、23時スタートの場合は前日の5時がfirst_wake_upになって、スタートより前の時間となってマークが行われない。
    if target_timespan.start < first_wake_up: 
        bitmap.sign_as_busy(
            timespan(
                target_timespan.start,
                first_wake_up
            )
        )

    cursor = datetime.combine(date=target_timespan.start,time=sleepSchedule.go_to_bed,tzinfo=target_timespan.start.tzinfo) #その日の就寝時間に合わせる
    # 0時スタート、5時起床の場合False
    # 23時スタート、5時起床の場合True
    # cursorがスタートした日付における就寝時間を取るためである。
    # つまり、0時スタートの場合はその日の睡眠時間はスキップしてしまう。
    if cursor < target_timespan.start:#就寝時間を超えていた場合->起床時間までマークし、次の日の就寝時間に合わせる
        bitmap.sign_as_busy(
            timespan(
                target_timespan.start,
                cursor + sleep_duration # 起床時間
            )
        )
        cursor += timedelta(days=1)

    while target_timespan.overlaps(cursor + sleep_duration):
        bitmap.sign_as_busy(
            timespan(
                cursor,
                cursor + sleep_duration
            )
        )
        cursor += timedelta(days=1)
        await sleep(0)
    
    if cursor < target_timespan.end:
        bitmap.sign_as_busy(
            timespan(
                cursor,
                target_timespan.end
            )
        )

    return bitmap