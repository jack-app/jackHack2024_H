from AssignmentEntryHandler.GoogleCalenderAPIWrapper import GoogleCalenderAPIClient
from AuthHandler.GoogleAPITokenHandler.tokenBundle import GoogleAPITokenBundle
from datetime import datetime, timezone, timedelta
from asyncio import run

ac_token = "ya29.a0AXooCgs4ZPNIxLI02jkHuHWx_orCUMMYVri_W629NyYBxAoheZDvpceRHe6ircvV2eXv9qTkdp_6hIG1IV9SYLk3jzNkVMLxSXdDAi8EYSZgN_zNHPYm51E9he7zzO_HHBxjlcNX_8qgShbossOZgDtmFC9GajDhf3ibaCgYKAcsSARESFQHGX2MiHK_M4zl_81FikhI9vtfVXA0171"#input("access token:")
rf_token = "1//0eumD7Z0fk-8kCgYIARAAGA4SNwF-L9IrkmwVBHHnTwQKRA2EEkTbQrWeLDgTwdWuD5j1YOsgyn-zU-7VYGxQJ603Ecgrko8C14Q"#input("refresh token:")

tokens = GoogleAPITokenBundle(ac_token,rf_token)
client = GoogleCalenderAPIClient(tokens)

up_to = datetime.now(timezone.utc) + timedelta(days=7)
colors = run(client._get_raw_colors())

print(colors)