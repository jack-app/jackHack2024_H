from secrets import token_hex
from .exceptions import StateNotExists
from .config import _POP_TRIAL_INTERVAL, _POP_TRIAL_LIMIT, _STATE_EXPIRY, _MAX_QUEUE_SIZE
from asyncio import sleep, get_running_loop
from datetime import datetime, timedelta
from typing import Dict

class Entry:
    code: str
    issuedAt: datetime
    state_expiry: timedelta
    def __init__(self, state_expiry: timedelta):
        self.code = None
        self.issuedAt = datetime.now()
        self.state_expiry = state_expiry
    def __hash__(self) -> int:
        return hash(self)
    def isExpired(self):
        return (datetime.now() - self.issuedAt) > self.state_expiry

class SignQueue:
    queue: Dict[str,Entry]
    pop_trial_interval: timedelta
    pop_trial_limit: int
    state_expiry: timedelta
    max_queue_size: int
    def __init__(
            self,
            pop_trial_interval: timedelta = timedelta(seconds=_POP_TRIAL_INTERVAL),
            pop_trial_limit: int = _POP_TRIAL_LIMIT,
            state_expiry: timedelta = timedelta(minutes=_STATE_EXPIRY),
            max_queue_size: int = _MAX_QUEUE_SIZE
    ):
        self.queue = {}
        self.pop_trial_interval = pop_trial_interval
        self.pop_trial_limit = pop_trial_limit
        self.state_expiry = state_expiry
        self.max_queue_size = max_queue_size
    
    def sizeSize(self):
        return len(self.queue)

    async def cleanUp(self):
        for state in list(self.queue.keys()):
            try:
                if self.queue[state].isExpired():
                    del self.queue[state]
            except KeyError: pass 
            await sleep(0) # to allow other tasks to block this task

    def issueState(self,state:str=token_hex()):
        self.queue[state] = Entry(self.state_expiry)
        if len(self.queue) > self.max_queue_size:
            get_running_loop().create_task(self.cleanUp())
        return state
    
    def sign(self, state:str, code:str):
        if state not in self.queue:
            raise StateNotExists(f"{state} is not in the queue.")
        self.queue[state].code = code

    async def pop(self,state):
        if state not in self.queue:
            raise StateNotExists(f"{state} is not in the queue.")
        
        try:
            for _ in range(self.pop_trial_limit):
                if self.queue[state].code is not None:
                    break
                await sleep(self.pop_trial_interval.total_seconds())
        except KeyError:
            raise StateNotExists(f"{state} is not in the queue.")
        
        if self.queue[state].code is None:
            raise TimeoutError(f"timeout. code is not set for {state} yet.")

        result = self.queue[state].code
        del self.queue[state]
        return result
