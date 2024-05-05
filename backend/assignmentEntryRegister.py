from shared.AssignmentEntry import AssignmentEntry
from google.oauth2.credentials import Credentials
from calenderapiwrapper.calender_event_generator import CalenderEventGenerator

# 追加に成功したらTrueを返してください。そうでなければFalse
def assignmentEntryRegister(assignmentEntry: AssignmentEntry, cred: Credentials)->bool:
    calendar = CalenderEventGenerator(cred)
    event = AssignmentEntry(
        id="1",
        title="課題1",
        courseName="Google Classroom",
        courseId="1",#これはなんだろう
        dueDate="2024-05-20 23:59:59",
        duration=60,
    )#MOCK
    calendar.write_event_to_calendar(event)