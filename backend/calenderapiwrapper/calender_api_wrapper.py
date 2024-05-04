import datetime
import os.path

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

  def read_calendar(self, time_max="2050-01-01T00:00:00+00:00"):
    try:
      service = build("calendar", "v3", credentials=self.creds)

      # Call the Calendar API
      now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
      print(f"{time_max}までの予定を取得します")
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
        print("No upcoming events found.")
        return

      # Prints the start and name of the next 10 events
      for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        print(start, end, event["summary"])

    except HttpError as error:
      print(f"An error occurred: {error}")

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
          'dateTime': '2024-05-09T00:00:00-07:00',
      },
      'end': {
          'dateTime': '2024-05-09T01:00:00-07:00',
      },
  }
  calendar.write_calendar(event)