from AssignmentEntryHandler.GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from AuthHandler.GoogleAPITokenHandler.tokenBundle import GoogleAPITokenBundle
from datetime import datetime, timezone, timedelta
from asyncio import run

ac_token = "ya29.a0AXooCgs1eC9uQ-hb-ZOvGiy-cuZlocmAzVtK-0SK-4hsVNjGllxxs5ZeXYm4_2XPSO2LXyCx0rAeE8Boh7DGU835inKnc1TUAQJhvyz0zmokns37nP5tqaEMw8-pZh46008isWdSkhIGWqM-GbSl9nDUj41MZLq4okWFaCgYKAVsSARESFQHGX2MiEx-Vbw3CArZjFwnac5ZG2w0171"#input("access token:")
rf_token = "1//0eQIT9tQLbwenCgYIARAAGA4SNwF-L9Iry2gKhRrc2s3TN1FVWj_JHKuwGhzsQ8s-WE0yubqA_iG3eYfNmC-l0Qh52IP_GhubOyo"#input("refresh token:")

tokens = GoogleAPITokenBundle(ac_token,rf_token)
client = GoogleCalenderAPIClient(tokens)

up_to = datetime.now(timezone.utc) + timedelta(days=7)
events = run(client._get_raw_busytimes(up_to))

for e in events:
    print(e)