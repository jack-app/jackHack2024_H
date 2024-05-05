import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request as GRequest
import requests
from shared.Exceptions import ReAuthentificationNeededException
from google.auth.exceptions import RefreshError
from fastapi import Response

load_dotenv('./GoogleAPITokenHandler/.env')

AUTH_FLOW = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            './GoogleAPITokenHandler/credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )
AUTH_FLOW.redirect_uri = os.environ['REDIRECT_URI']

ACCESS_TOKEN="access_token"
REFRESH_TOKEN="refresh_token"

def construct_cledentials(access_token,refresh_token):
    return google.oauth2.credentials.Credentials(
        access_token,
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET']
    )

def revoke(access_token):
    requests.post('https://oauth2.googleapis.com/revoke',
        params={'token': access_token},
        headers = {'content-type': 'application/x-www-form-urlencoded'})

def refresh(cred: google.oauth2.credentials.Credentials):
    try:
        cred.refresh(GRequest())
    except RefreshError as error:
        raise ReAuthentificationNeededException("token-refresh failed. please re-authenticate.")

def tokensExist(cookies, response: Response):
    if REFRESH_TOKEN not in cookies:
        response.status_code = 401
        raise ReAuthentificationNeededException("refresh_token cookie is not found")
    if ACCESS_TOKEN not in cookies:
        response.status_code = 401
        raise ReAuthentificationNeededException("access_token cookie is not found")
