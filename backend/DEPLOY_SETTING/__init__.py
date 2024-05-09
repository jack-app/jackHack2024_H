from os import environ as __environ
from dotenv import load_dotenv as __load_dotenv

__load_dotenv('./DEPLOY_SETTING/.env')

CLIENT_ID = __environ['CLIENT_ID']
CLIENT_SECRET = __environ['CLIENT_SECRET']
REDIRECT_URI = __environ['REDIRECT_URI']
CREDENTIAL_FILE_PATH = './DEPLOY_SETTING/credentials.json'