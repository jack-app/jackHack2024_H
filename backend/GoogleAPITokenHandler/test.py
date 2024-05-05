# This file is used to test the GoogleApiTokenGetter class
import asyncio
from GoogleAPITokenHandler.main import AuthFlowSource,GoogleApiTokenPopper,construct_cledentials

tokenGetter = AuthFlowSource()
print(tokenGetter.get_oauth_url())
code = input("code")
state = input("state")
AuthFlowSource.sign(state, code)
tokenBundle = asyncio.run(tokenGetter.issue_gapi_tokens())
print(tokenBundle.access_token)
print(tokenBundle.refresh_token)

credentials = construct_cledentials(tokenBundle)

from calenderapiwrapper.assignmentEntryRegister import assignmentEntryRegister
from shared.AssignmentEntry import AssignmentEntry

ae = AssignmentEntry(
        id="1",
        title="課題1",
        courseName="Google Classroom",
        courseId="1",#これはなんだろう
        dueDate="2024-05-20 23:59:59",
        duration=60
)#MOCK

assignmentEntryRegister(ae, credentials)
