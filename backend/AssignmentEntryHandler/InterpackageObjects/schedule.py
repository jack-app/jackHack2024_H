from datetime import datetime,timedelta
from typing import overload
from math import ceil

class timespan:
    """
    Timespan is delt as a closure of start and end. That means the start is included and the end is ALSO included.
    """
    def __init__(self, start:datetime, end:datetime):
        if start > end: raise ValueError(f"start is later than end: {start.isoformat()} > {end.isoformat()}")
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
        when force is True, the timespan is concatenated regardless of the continuity.
        """
        if force or self.end == other.start:
            return timespan(self.start,other.end)
        raise ValueError(f"timespan is not continuous: {self.end} != {other.start}")

class _spanIndex:
    def __init__(self, index:int, onBoundary:bool):
        """
        when onBoundary is True, the time is between index-1 and index.
        """
        self.index = index
        self.onBoundary = onBoundary

class FreeBusyBitMap:
    def __init__(self, scope: timespan, interval:timedelta):
        self.bitMap = 0b0 # free = 0, busy = 1. each bit represents each span.
        self.scope = scope
        self.interval = interval
        self.length = ceil(scope.duration() / interval)

    @overload
    def overlaps(self, target:datetime) -> None: ...
    @overload
    def overlaps(self, target:timespan) -> None: ...
    def overlaps(self, target):
        if isinstance(target, timespan):
            if not self.scope.overlaps(target):
                raise ValueError(f"time is not in scope: {target} is not in {self.scope}")
            return
        if isinstance(target, datetime):
            if not self.scope.overlaps(target):
                raise ValueError(f"time is not in scope: {target.isoformat()} is not in {self.scope}")

    def fall_into_which_span(self, time:datetime):
        self.overlaps(time)
        index = (time - self.scope.start) // self.interval
        rest = (time - self.scope.start) % self.interval
        return _spanIndex(index, rest == timedelta(0)) 
    
    def sign_as_busy(self, span:timespan):
        self.overlaps(span)

        first_span = self.fall_into_which_span(span.start)
        last_span = self.fall_into_which_span(span.end)

        if first_span.onBoundary and first_span.index > 0:    
            scope_start_to_first = (1 << first_span.index-1) - 1 # not includes first_span.index-1
        else:
            scope_start_to_first = (1 << first_span.index) - 1 # not includes first_span.index
        
        if last_span.index < self.length:
            scope_start_to_last = (1 << last_span.index+1) - 1 # includes last_span.index
        else:
            scope_start_to_last = (1 << last_span.index) - 1 # not includes last_span.index
        
        first_span_to_last = scope_start_to_last - scope_start_to_first
        self.bitMap |= first_span_to_last

    def index_to_timespan(self, index:int):
        if index >= self.length: raise ValueError(f"index is out of range: {index} >= {self.length}")
        
        up_to = None
        if index == self.length-1:
            up_to = self.scope.end
        else:
            up_to = self.scope.start + self.interval * (index+1)

        return timespan(
            self.scope.start + self.interval * index,
            up_to
        )

    def get_free_timespans(self):
        current = None
        for i in range(self.length):
            if (self.bitMap >> i) & 1:# i-th bit is 1 : busy
                if current is None: pass
                else:
                    yield current
                    current = None
            else: # i-th bit is 0 : free
                if current is None:
                    current = self.index_to_timespan(i)
                else:
                    current = current.concat(self.index_to_timespan(i))
        if current is not None:
            yield current

    def reverse(self):
        currentMap = self.bitMap
        self.sign_as_busy(self.scope)
        self.bitMap = self.bitMap ^ currentMap
        return self
    
    def clone(self):
        newMap = FreeBusyBitMap(self.scope,self.interval)
        newMap.bitMap = self.bitMap
        return newMap
    def __not__(self):
        newMap = self.clone() # not to destruct the original object.
        return newMap.reverse()
    def is_consistent_with(self, other:'FreeBusyBitMap'):
        if self.scope.start != other.scope.start or self.scope.end != other.scope.end: 
            raise ValueError(f"scope is not the same: {self.scope} != {other.scope}")
        if self.interval != other.interval: raise ValueError(f"timespan is not the same: {self.interval} != {other.interval}")
    def __and__(self, other:'FreeBusyBitMap'):
        self.is_consistent_with(other)
        newMap = self.clone() # not to destruct the original object.
        newMap.bitMap &= other.bitMap
        return newMap
    def __or__(self, other:'FreeBusyBitMap'):
        self.is_consistent_with(other)
        newMap = self.clone() # not to destruct the original object.
        newMap.bitMap |= other.bitMap
        return newMap
    def __xor__(self, other:'FreeBusyBitMap'):
        self.is_consistent_with(other)
        newMap = self.clone() # not to destruct the original object.
        newMap.bitMap ^= other.bitMap
        return newMap
    def __str__(self):
        return (
            self.scope.start.isoformat() + "->" 
            + ('{:0'+str(self.length)+'b}').format(self.bitMap)[::-1]
            + "->" + self.scope.end.isoformat()
        )