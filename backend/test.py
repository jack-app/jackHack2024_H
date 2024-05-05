from shared.AssignmentEntry import AssignmentEntry
from GoogleAPITokenHandler.main import ACCESS_TOKEN, REFRESH_TOKEN

mockAssignmentEntry = AssignmentEntry(
    id="1",
    title="課題1",
    courseName="Google Classroom",
    courseId="1",#これはなんだろう
    dueDate="2024-05-20 23:59:59",
    duration=600,
)
from json import loads
entry = loads(mockAssignmentEntry.model_dump_json())

import requests

print("access and authorize this app: http://localhost:8000/redirectToAuthURL")
token = input("accessToken:")
refresh_token = input("refreshToken:")
print(entry)
res = requests.post(
    url="http://localhost:8000/register",
    json=entry,
    cookies={ACCESS_TOKEN:token,
             REFRESH_TOKEN:refresh_token},
    headers={"Content-Type":"application/json"}
)
print(res.text)
