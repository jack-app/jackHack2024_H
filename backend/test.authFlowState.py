from GAPITokenHandler.authFlowState import * 
import asyncio

async def main():
    for i in range(100):
        issueStateToQueue(i)
    while True:
        print(queueSize())
        await asyncio.sleep(1)

asyncio.run(main())