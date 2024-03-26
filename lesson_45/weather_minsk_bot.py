import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton

from .weather_util import get_weather

TOKEN = getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


MINSK_WEATHER_KEY = 'minks_weather'


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = [[InlineKeyboardButton(text='Weather in Minsk', callback_data=MINSK_WEATHER_KEY)]]

    await message.answer(f"Hello, I'm weather bot. I can say you weather in Minks!",
                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard))


@dp.callback_query(F.data == MINSK_WEATHER_KEY)
async def echo_handler(callback: types.CallbackQuery) -> None:
    minsk_temperature = await get_weather(city='Minsk')
    await callback.message.answer(f'Weather in minsk now: {minsk_temperature}°C')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
