# This file is used to test the GoogleApiTokenGetter class
import asyncio
from google_api_token_getter.main import AuthFlowSource,GoogleApiTokenPopper,construct_cledentials

tokenGetter = AuthFlowSource()
print(tokenGetter.get_oauth_url())
code = input("code")
state = input("state")
AuthFlowSource.sign(state, code)
tokenBundle = asyncio.run(tokenGetter.issue_gapi_tokens())
print(tokenBundle.access_token)
print(tokenBundle.refresh_token)

credentials = construct_cledentials(tokenBundle)
tokenPopper = GoogleApiTokenPopper(tokenBundle)

print(tokenPopper.pop())