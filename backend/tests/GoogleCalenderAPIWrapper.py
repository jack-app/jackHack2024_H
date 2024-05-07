from AssignmentEntryHandler.GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from AuthHandler.GoogleAPITokenHandler.tokenBundle import GoogleAPITokenBundle
from datetime import datetime, timezone, timedelta
from asyncio import run

ac_token = "ya29.a0AXooCgvkDnJfjpig8hTNCyQwya__q2cbBbB_el-9D0fzdaaOOWnTEzyWQOiyyJUecyAJ0SAaE2mH_FfL0O9_r8LTeGXDXHOQdWMOcV31ZgKoDdXDZibhKYejPv_nM9dKQBBxbT9e1VLajKrSqsxIsuasVK20ub91r6bzaCgYKAcoSARISFQHGX2MiglXjVJPg0OTG9ZeH7aDfwg0171"#input("access token:")
rf_token = "1//0e24YPhCQ1BDuCgYIARAAGA4SNwF-L9Ir7_gHehNjuWrE3Qc9S_qrF5YmjBNOCfxneHiRDBIUsYUon3dIbVqhsSQvEE-jB7Kzg5k"#input("refresh token:")

tokens = GoogleAPITokenBundle(ac_token,rf_token)
client = GoogleCalenderAPIClient(tokens)

up_to = datetime.now(timezone.utc) + timedelta(days=7)
events = run(client._get_raw_busytimes(up_to))

for e in events:
    print(e)