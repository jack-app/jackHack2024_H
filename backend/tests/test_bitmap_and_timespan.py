from AssignmentRegister.InterpackageObject.datetime_expansion import timespan
from AssignmentRegister.CalenderEventGenerator.CalenderEventScheduler.bitmap import FreeBusyBitMap
from datetime import datetime,timedelta

async def test():
    origin = datetime.now()

    scope = timespan(origin,origin+timedelta(hours=24,minutes=30))

    fb0 = FreeBusyBitMap(scope,timedelta(hours=1))
    fb0._sign_as_busy(
        timespan(origin+timedelta(hours=5,microseconds=1),origin+timedelta(hours=8))
    )

    fb1 = FreeBusyBitMap(scope,timedelta(hours=1))
    fb1._sign_as_busy(
        timespan(origin+timedelta(hours=7),origin+timedelta(hours=10))
    )

    fb2 = FreeBusyBitMap(scope,timedelta(hours=1))
    fb2._sign_as_busy(
        timespan(origin+timedelta(hours=15),origin+timedelta(hours=18))
    )

    print((fb0))
    print((fb0&fb1))
    print((fb0&fb1|fb2))
    async for span in (fb0&fb1|fb2).get_free_chunks():
        print(span)
    print((fb0&fb1|fb2).reverse())
    async for span in (fb0&fb1|fb2).reverse().get_free_chunks():
        print(span)
    print((fb0&fb1|fb2).length)

from asyncio import run
run(test())