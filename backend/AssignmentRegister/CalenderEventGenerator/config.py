from ..InterpackageObject.dataTransferObject import SleepSchedule
from datetime import time

DEFAULT_SLEEP_SCHEDULE = SleepSchedule(
    go_to_bed=time(hour=22,minute=0),
    wake_up=time(hour=8,minute=0)
)