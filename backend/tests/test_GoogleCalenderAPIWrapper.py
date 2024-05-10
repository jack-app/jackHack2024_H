from tests.module_get_token import get_tokenBundle
from AssignmentHandler.GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from datetime import datetime,timedelta,timezone
from asyncio import run

client = GoogleCalenderAPIClient(get_tokenBundle())

up_to = datetime.now(timezone.utc) + timedelta(days=7)
colors = run(client._get_raw_colors())

print(colors)