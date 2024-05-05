from calenderapiwrapper.calender_event_generator import CalenderEventGenerator
from shared.AssignmentEntry import AssignmentEntry

creds = "dummy"
calendar = CalenderEventGenerator(creds)
event = AssignmentEntry(
    id="1",
    title="課題1",
    courseName="Google Classroom",
    courseId="1",#これはなんだろう
    dueDate="2024-05-20 23:59:59",
    duration=600,
)
calendar.write_event_to_calendar(event)