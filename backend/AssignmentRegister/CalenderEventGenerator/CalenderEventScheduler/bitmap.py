
from ...InterpackageObject.datetime_expansion import timespan
from datetime import datetime,timedelta
from pydantic import BaseModel
from typing import overload
from math import ceil
from asyncio import sleep

class FreeBusyBitMap:
    """
    扱うdatetimeはすべて秒以下を切り捨てる。
    """
    bitMap:int
    scope:timespan
    interval:timedelta
    length:int

    # それぞれのbitがそれぞれの時間的区間を表す.bitが表す時間的区間をcellと呼称する。
    # 一つ以上の連続したcellを結合してできた連続した区間をchunkと呼称する。

    def __init__(self, scope: timespan, interval:timedelta):
        self.bitMap = 0b0 # free = 0, busy = 1. 
        self.scope = scope 
        self.interval = interval 
        self.length = ceil(scope.duration() / interval)

    @overload
    def _overlap_assertion(self, target:datetime) -> None: ...
    @overload
    def _overlap_assertion(self, target:timespan) -> None: ...
    def _overlap_assertion(self, target):
        if isinstance(target, timespan):
            if not self.scope.overlaps(target):
                raise ValueError(f"timespan is not in scope: {target} is not in {self.scope}")
            return
        if isinstance(target, datetime):
            if not self.scope.overlaps(target):
                raise ValueError(f"time is not in scope: {target.isoformat()} is not in {self.scope}")
    class __cellIndex(BaseModel): # データのアノテーションのためだけに使っている
        """
        onBoundaryがTrueの時、timeはindex-1とindexのspanのちょうど境にある。
        """
        index:int
        onBoundary:bool

    def get_cell_index_of(self, time:datetime):
        self._overlap_assertion(time)
        index = (time - self.scope.start) // self.interval
        rest = (time - self.scope.start) % self.interval
        return self.__cellIndex(index= index,onBoundary= rest == timedelta(0)) 
    
    def sign_as_busy_safely(self, span:timespan):
        # spanがscopeの外にある場合にも対応する。
        # もともと用いられていたsign_as_busyを_sign_as_busyとして内部に隠蔽し、
        # このメソッドを公開してエラー/複雑なロジックの漏れ出しを防ぐ。
        if span.end < self.scope.start or self.scope.end < span.start: return
        if self.scope.start > span.start:
            span = timespan(self.scope.start,span.end)
        if self.scope.end < span.end:
            span = timespan(span.start,self.scope.end)
        self._sign_as_busy(span)

    def _sign_as_busy(self, span:timespan):

        first_span = self.get_cell_index_of(span.start)
        last_span = self.get_cell_index_of(span.end)

        if first_span.onBoundary and first_span.index > 0:    
            scope_start_to_first = (1 << first_span.index-1) - 1 # first_span.index-1 を含まない
        else:
            scope_start_to_first = (1 << first_span.index) - 1 # first_span.index を含まない
        
        if last_span.index < self.length:
            scope_start_to_last = (1 << last_span.index+1) - 1 # last_span.index　を含む
        else:
            scope_start_to_last = (1 << last_span.index) - 1 # last_span.index を含まない
        
        first_span_to_last = scope_start_to_last - scope_start_to_first
        self.bitMap |= first_span_to_last

    def cast_bit_index_to_cell(self, index:int):
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

    async def get_free_chunks(self):
        current = None
        for i in range(self.length):
            if (self.bitMap >> i) & 1:# i番目の bit が 1 : i番目の時間区間においてbusy
                if current is None: pass
                else:
                    yield current
                    current = None
            else: # i番目の bit が 0 : i番目の時間区間においてfree
                if current is None:
                    current = self.cast_bit_index_to_cell(i)
                else:
                    current = current.concat(self.cast_bit_index_to_cell(i))
            await sleep(0)
        if current is not None:
            yield current

    # 破壊的に反転する
    # 隠蔽するべきか？

    def reverse(self):
        """注意: 破壊的"""
        currentMap = self.bitMap
        self._sign_as_busy(self.scope)
        self.bitMap = self.bitMap ^ currentMap
        return self
    
    # 以下演算子オーバーロード。演算子はすべて非破壊的。

    def clone(self):
        newMap = FreeBusyBitMap(self.scope,self.interval)
        newMap.bitMap = self.bitMap
        return newMap
    def __not__(self):
        newMap = self.clone() # 元のオブジェクトを破壊しないために。
        return newMap.reverse()
    def is_consistent_with(self, other:'FreeBusyBitMap'):
        if self.scope.start != other.scope.start or self.scope.end != other.scope.end: 
            raise ValueError(f"scope is not the same: {self.scope} != {other.scope}")
        if self.interval != other.interval: raise ValueError(f"timespan is not the same: {self.interval} != {other.interval}")
    def __and__(self, other:'FreeBusyBitMap'):
        self.is_consistent_with(other)
        newMap = self.clone() # 元のオブジェクトを破壊しないために。
        newMap.bitMap &= other.bitMap
        return newMap
    def __or__(self, other:'FreeBusyBitMap'):
        self.is_consistent_with(other)
        newMap = self.clone() # 元のオブジェクトを破壊しないために。
        newMap.bitMap |= other.bitMap
        return newMap
    def __xor__(self, other:'FreeBusyBitMap'):
        self.is_consistent_with(other)
        newMap = self.clone() # 元のオブジェクトを破壊しないために。
        newMap.bitMap ^= other.bitMap
        return newMap
    def __str__(self):
        return (
            self.scope.start.isoformat() + "->" 
            + ('{:0'+str(self.length)+'b}').format(self.bitMap)[::-1]
            + "->" + self.scope.end.isoformat()
        )