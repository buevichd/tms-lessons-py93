import asyncio

import requests
import time
import aiohttp


cities = ['Moscow', 'St. Petersburg', 'Rostov-on-Don', 'Kaliningrad', 'Vladivostok',
         'Minsk', 'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York']

URL_PATTERN = 'https://api.openweathermap.org/data/2.5/weather' \
              '?appid=2a4ff86f9aaa70041ec8e82db64abf56&q={city}&units=metric'

def sync_loading():
    for city in cities * 5:
        response = requests.get(URL_PATTERN.format(city=city)).json()
        print(f'Temperature in {city}: {response["main"]["temp"]}C')


async def async_loading():
    async with aiohttp.ClientSession() as session:
        for city in cities * 5:
            async with session.get(URL_PATTERN.format(city=city)) as response:
                response = await response.json()
                print(f'Temperature in {city}: {response["main"]["temp"]}C')


start_time = time.time()
# sync_loading()
asyncio.run(async_loading())
finish_time = time.time()
print(f'Total time: {finish_time - start_time}')
