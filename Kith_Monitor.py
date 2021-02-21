from Kith_Class import  mens_apparel, footwear
import asyncio
import time


async def tasks():
 task1 = asyncio.create_task(mens_apparel.availability_check())
 task2 = asyncio.create_task(footwear.availability_check())
 await task1
 await task2

# asyncio.run(tasks())

loop = asyncio.get_event_loop()
while True:
	loop.run_until_complete(tasks())
	time.sleep(8)
	
