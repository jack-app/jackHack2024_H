# This file is used to test the GoogleApiTokenGetter class
import asyncio
from google_api_token_getter.main import GoogleApiTokenGetter

tokenGetter = GoogleApiTokenGetter()
print(tokenGetter.get_oauth_url())
code = input("code")
state = input("state")
GoogleApiTokenGetter.sign(state, code)
tokenBundle = asyncio.run(tokenGetter.get_token())
print(tokenBundle.access_token)
print(tokenBundle.refresh_token)
print(tokenBundle.expires_at)