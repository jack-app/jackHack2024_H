from tests.module_get_token import get_tokenBundle
from AssignmentRegister.GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from datetime import datetime,timedelta,timezone
from asyncio import run

client = GoogleCalenderAPIClient(get_tokenBundle())

up_to = datetime.now(timezone.utc) + timedelta(days=7)

print(run(client._get_raw_colors()))
print(run(client._get_raw_busytimes(up_to)))
print(run(client._get_raw_events(up_to)))
print(run(client._get_calender_ids()))