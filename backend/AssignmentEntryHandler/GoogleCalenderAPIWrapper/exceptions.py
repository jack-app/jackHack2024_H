from aiohttp import ClientResponse
from datetime import datetime
from asyncio import run,get_running_loop

class InvalidToken(Exception):
    http_status = 401
class TooManyEvents(Exception):
    http_status = 500
class UnexpectedAPIResponce(Exception):
    http_status = 500
class ReAuthorizationRequired(Exception):
    http_status = 401
class TimeZoneUnspecified(Exception):
    def __init__(self, time:datetime):
        self.msg = f"timezone is not specified in {time.isoformat()}"
    http_status = 500