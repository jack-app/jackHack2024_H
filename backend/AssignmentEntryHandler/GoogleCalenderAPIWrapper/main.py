from ..calenderEvent import CalenderEvent
from ..schedule import timespan
from .exceptions import ReAuthorizationRequired, UnexpectedAPIResponce, TimeZoneUnspecified
from datetime import datetime, timezone
from AuthHandler import GoogleAPITokenBundle
from aiohttp import request
from asyncio import sleep

class GoogleCalenderAPIClient:
    def __init__(self, tokenBundle:GoogleAPITokenBundle):
        self.tokens = tokenBundle
        self.default_headers = {
            "Authorization":f"Bearer {self.tokens.access_token}",
            "Content-Type":"application/json"
        }
    
    async def _get_raw_events(self,earlier_than:datetime):
        
        if earlier_than.tzinfo is None: raise TimeZoneUnspecified(earlier_than)
        
        async with request(
            "GET",
            "https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events"
            .format(calendarId="primary"),
            headers=self.default_headers,
            params={
                "timeMin":datetime.now(timezone.utc).isoformat(),
                "timeMax":earlier_than.isoformat(),
                "maxResults":2500,# Maximum value of maxResults is 2500
                "singleEvents":'true',
                "orderBy":"startTime"
            }
        ) as resp:
            if resp.status == 200:
                events = await resp.json()
                if "nextPageToken" in events:
                    raise Exception("There were too many events to fetch.")
                return events["items"]
            if resp.status == 401:
                raise ReAuthorizationRequired(await resp.text())
            raise UnexpectedAPIResponce(await resp.text())
        


    async def get_events(self,earlier_than:datetime):
        """
        if the event is all day event, it will be ignored.
        "all day event" means that the event has no "dateTime" field in "start" and "end" field.
        """
        for raw_event_entry in await self._get_raw_events(earlier_than):
            try:
                yield CalenderEvent(
                    title=raw_event_entry["summary"],
                    description=raw_event_entry.get("description", None),
                    start=datetime.fromisoformat(raw_event_entry["start"]["dateTime"]),
                    end=datetime.fromisoformat(raw_event_entry["end"]["dateTime"])
                )
            except KeyError: pass
            await sleep(0) # to allow other tasks to block this task.

    async def _get_calender_ids(self):
        calenders = []
        async with request(
            "GET",
            "https://www.googleapis.com/calendar/v3/users/me/calendarList",
            headers=self.default_headers
        ) as resp:
            if resp.status == 200:
                calenders = await resp.json()
                return [calender["id"] for calender in calenders["items"]]
            if resp.status == 401:
                raise ReAuthorizationRequired(await resp.text())
            raise UnexpectedAPIResponce(await resp.text())

    async def _get_raw_busytimes(self,up_to:datetime):
        # https://developers.google.com/calendar/api/v3/reference/freebusy/query

        if up_to.tzinfo is None: raise TimeZoneUnspecified(up_to)

        async with request(
            "POST",
            "https://www.googleapis.com/calendar/v3/freeBusy",
            headers=self.default_headers,
            json={
                "timeMin":datetime.now(timezone.utc).isoformat(),
                "timeMax":up_to.isoformat(),
                "items":[
                    {"id":"primary"}
                ]
            }
        ) as resp:
            if resp.status == 200:
                freebuzy = await resp.json()
                return freebuzy["calendars"]["primary"]["busy"]
            if resp.status == 401:
                raise ReAuthorizationRequired(await resp.text())
            raise UnexpectedAPIResponce(await resp.text())


    async def get_busytimes(self,up_to:datetime):
        for raw_busytime in await self._get_raw_busytimes(up_to):
            yield timespan(
                start=datetime.fromisoformat(raw_busytime["start"]),
                end=datetime.fromisoformat(raw_busytime["end"])
            )
    
    async def register_event(self, event:CalenderEvent)->str:
        async with request(
            "POST",
            "https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events"
            .format(calendarId="primary"),
            headers=self.default_headers,
            json={
                "summary": event.title,
                "description": event.description or "",
                "end": {
                    "dateTime":event.end.isoformat()
                },
                "start": {
                    "dateTime":event.start.isoformat()
                },
                "reminders": {
                    "useDefault": 'true'
                }
            }
        ) as resp:
            if resp.status == 200:
                result = await resp.json()
                return result["id"]
            if resp.status == 401:
                raise ReAuthorizationRequired(await resp.text())
            raise UnexpectedAPIResponce(await resp.text())
        