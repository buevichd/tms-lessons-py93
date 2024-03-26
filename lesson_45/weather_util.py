import aiohttp


async def get_weather(city=None, lat=None, lon=None) -> float:
   url = 'https://api.openweathermap.org/data/2.5/weather' \
         '?appid=2a4ff86f9aaa70041ec8e82db64abf56&units=metric'
   if city is not None:
       url += f'&q={city}'
   elif lat is not None and lon is not None:
       url += f'&lat={lat}&lon={lon}'
   else:
       raise Exception('city or lat/lon must be specified')
   async with aiohttp.ClientSession() as session:
       async with session.get(url) as response:
           weather_json = await response.json()
           return weather_json['main']['temp']
