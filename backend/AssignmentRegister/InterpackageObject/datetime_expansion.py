from datetime import datetime
from typing import overload

class timespan:
    """
    timespanはstartとendの閉包として扱われる。つまりstartは含まれ、endも含まれる。
    """
    start:datetime
    end:datetime
    
    def __init__(self, start:datetime, end:datetime):
        if start > end:
            raise ValueError(f"start is later than end: {start.isoformat()} > {end.isoformat()}")
        self.start = start
        self.end = end
    
    @overload
    def overlaps(self, target:datetime) -> bool: ...
    @overload
    def overlaps(self, target:'timespan') -> bool: ...
    def overlaps(self, target):
        if isinstance(target, timespan):
            return self.start <= target.start and target.end <= self.end
        if isinstance(target, datetime):
            return self.start <= target <= self.end
        raise ValueError(f"target is not datetime or timespan: {target}")
    def duration(self):
        return self.end - self.start
    def __str__(self):
        return self.start.isoformat() + "->" + self.end.isoformat()
    def concat(self, other:'timespan', force:bool=False):
        """
        forceがTrueの時、連続性を無視してtimespanを連結する。
        """
        if force or self.end == other.start:
            return timespan(self.start,other.end)
        raise ValueError(f"timespan is not continuous: {self.end} != {other.start}")
