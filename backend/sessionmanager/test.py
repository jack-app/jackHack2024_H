import time
import datetime
now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
now = now+datetime.timedelta(days=5)
print(now > datetime.datetime.now())
