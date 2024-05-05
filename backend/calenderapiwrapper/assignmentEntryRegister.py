from shared.AssignmentEntry import AssignmentEntry
from google.oauth2.credentials import Credentials
from calenderapiwrapper.calender_event_generator import CalenderEventGenerator

def assignmentEntryRegister(assignmentEntry: AssignmentEntry, cred: Credentials):
    calendar = CalenderEventGenerator(cred)
    calendar.write_event_to_calendar(assignmentEntry)