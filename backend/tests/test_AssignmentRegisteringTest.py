from AssignmentHandler.GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from AuthHandler.GoogleAPITokenHandler.tokenBundle import GoogleAPITokenBundle
import requests
from tests.module_get_token import get_tokens_asDict
from datetime import datetime,timedelta,timezone

res = requests.post(
    "http://localhost:8000/register",
    json={
        "course_name":"mock course",
        "title_of_assignment":"mock assignment",
        "dueDate":(datetime.now(timezone.utc)+timedelta(days=2)).isoformat(),
        "duration":timedelta(hours=1).total_seconds(),
    },
    cookies=get_tokens_asDict()
)
print(res)
print(res.json())