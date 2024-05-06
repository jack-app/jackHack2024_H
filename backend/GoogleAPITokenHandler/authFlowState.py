from secrets import token_hex
from GoogleAPITokenHandler.exceptions import StateNotExists
from asyncio import sleep, get_running_loop
from datetime import datetime
from typing import Dict

_POP_TRIAL_INTERVAL = 1 # SEC
_POP_TRIAL_LIMIT = 10 # TIMES
_STATE_EXPIRY = 5*60 # SEC
_QUEUE_MAX_SIZE = 20 

class Entry:
    def __init__(self):
        self.code = None
        self.issuedAt = datetime.now()
    def __hash__(self) -> int:
        return hash(self)
    def isExpired(self):
        return (datetime.now() - self.issuedAt).seconds > _STATE_EXPIRY

_QUEUE: Dict[str, Entry] = {}

def queueSize():
    global _QUEUE
    return len(_QUEUE)

async def __cleanUp():
    global _QUEUE
    for state in list(_QUEUE.keys()):
        try:
            if _QUEUE[state].isExpired():
                del _QUEUE[state]
        except KeyError: pass
        await sleep(0.1) # to allow other tasks to run

def issueStateToQueue(state=None):
    global _QUEUE
    if state is None:
        state = token_hex()
    _QUEUE[state] = Entry()
    if len(_QUEUE) > _QUEUE_MAX_SIZE:
        get_running_loop().create_task(__cleanUp())
    return state

def signStateQueue(state, code):
    global _QUEUE
    if state not in _QUEUE:
        raise StateNotExists(f"{state} is not in the queue.")
    _QUEUE[state].code = code

async def popCode(state):
    global _QUEUE
    if state not in _QUEUE:
        raise StateNotExists(f"{state} is not in the queue.")
    
    try:
        for _ in range(_POP_TRIAL_LIMIT):
            if _QUEUE[state].code is not None:
                break
            await sleep(_POP_TRIAL_INTERVAL)
    except KeyError:
        raise StateNotExists(f"{state} is not in the queue.")
    
    if _QUEUE[state].code is None:
        raise TimeoutError(f"timeout. code is not set for {state} yet.")

    result = _QUEUE[state].code
    del _QUEUE[state]
    return result