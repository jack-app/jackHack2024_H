from os import environ
from dotenv import load_dotenv

load_dotenv('./DEPLOY_SETTING/.env')

CLIENT_ID = environ['CLIENT_ID']
CLIENT_SECRET = environ['CLIENT_SECRET']
REDIRECT_URI = environ['REDIRECT_URI']
CREDENTIAL_FILE_PATH = './DEPLOY_SETTING/credentials.json'