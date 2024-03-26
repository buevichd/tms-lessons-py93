import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton

from weather_util import get_weather

TOKEN = getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

MINSK_WEATHER_KEY = 'minks_weather'


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = [[KeyboardButton(text='Get weather', request_location=True)]]
    await message.answer(f"Hello, I'm weather bot. I can say you weather in your location!",
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=keyboard))


@dp.message(F.location)
async def echo_handler(message: Message) -> None:
    temperature = await get_weather(lat=message.location.latitude,
                                    lon=message.location.longitude)
    await message.answer(f'Weather at your location: {temperature}°C')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
