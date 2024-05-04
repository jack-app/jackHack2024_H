import datetime
import os.path
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import dateutil.parser

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class CalenderAPIWrapper:
  def __init__(self):
    #Google Calendar API.
    self.creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
      self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not self.creds or not self.creds.valid:
      if self.creds and self.creds.expired and self.creds.refresh_token:
        self.creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        self.creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(self.creds.to_json())

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

      if not events:
        print("No upcoming events found.", file=sys.stderr)
        return

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


if __name__ == "__main__":
  """
  calendar_api_wrapper.pyの関数一覧
  def __init__(self):
    -> カレンダーのAPIを使うための初期設定を行う

  def read_calendar(self, time_max):
    -> カレンダーのイベントを取得する(現在時刻からtime_maxまでのイベントを取得する)

  def write_calendar(self, event):
    -> カレンダーにイベントを書き込む
  """
  calendar = CalenderAPIWrapper()
  calendar.read_calendar()

  # イベントデータを作成(CalenderEventGeneratorで作成するようにする)
  event = {
      'summary': 'Google I/O 2019',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
          'dateTime': '2024-05-09T00:00:00+09:00',
      },
      'end': {
          'dateTime': '2024-05-09T01:00:00+09:00',
      },
  }
  calendar.write_calendar(event)