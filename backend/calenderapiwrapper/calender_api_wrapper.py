import datetime
import os.path
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import dateutil.parser

# If modifying these scopes
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class CalenderAPIWrapper:
  def __init__(self, creds):
    #Google Calendar API.
    self.creds = creds

  def read_calendar(self, time_max="2024-05-23T00:00:00+09:00"):
    calendar_info = {}
    try:
      service = build("calendar", "v3", credentials=self.creds)

      # Call the Calendar API
      now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
      start_time = dateutil.parser.parse(now)
      calendar_info["start_time"] = [start_time.year, start_time.month, start_time.day, start_time.hour, start_time.minute, 0]
      end_time = dateutil.parser.parse(time_max)
      calendar_info["end_time"] = [end_time.year, end_time.month, end_time.day, end_time.hour, end_time.minute, 0]
      events_result = (
          service.events()
          .list(
              calendarId="primary",
              timeMin=now,
              timeMax=time_max,
              singleEvents=True,
              orderBy="startTime",
          )
          .execute()
      )
      events = events_result.get("items", [])

      

      # Prints the start and name of the next 10 events
      calendar_info["events"] = []
      for event in events:
        start = dateutil.parser.parse(event["start"].get("dateTime", event["start"].get("date")))
        start = [start.year, start.month, start.day, start.hour, start.minute, 0]
        end = dateutil.parser.parse(event["end"].get("dateTime", event["end"].get("date")))
        end = [end.year, end.month, end.day, end.hour, end.minute, 0]


        event_info = {}
        event_info["start"] = start
        event_info["end"] = end
        calendar_info["events"].append(event_info)


    except HttpError as error:
      print(f"An error occurred: {error}", file=sys.stderr)


    return calendar_info

  def write_calendar(self, event):
    #eventの内容をカレンダーに書き込む
    service = build('calendar', 'v3', credentials=self.creds)
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created done')