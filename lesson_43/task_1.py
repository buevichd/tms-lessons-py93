import random
import asyncio
import time


async def wait_n_seconds():
    n = random.randint(1, 10)
    print(f'Start waiting {n} seconds')
    await asyncio.sleep(n)
    print(f'Finished waiting {n} seconds')


async def main():
    tasks = [asyncio.create_task(wait_n_seconds()) for i in range(100)]
    for task in tasks:
        await task


start_time = time.time()
asyncio.run(main())
end_time = time.time()
print(f'All tasks finished in {end_time - start_time} seconds')
