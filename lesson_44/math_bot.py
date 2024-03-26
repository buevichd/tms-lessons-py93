import asyncio
import logging
import os
import random

from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from aiogram import Dispatcher, Bot, F

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

class ConversationState(StatesGroup):
    wait_answer = State()


async def ask_math_question(message: Message, state: FSMContext):
    left = random.randint(1, 10)
    right = random.randint(1, 10)
    expected_answer = left + right

    await state.update_data({'expected_answer': expected_answer})

    await message.answer(f'{left} + {right} = ?')


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.set_state(ConversationState.wait_answer)
    await message.answer("Hi! My name is Math Bot.")
    await ask_math_question(message, state)


@dp.message(ConversationState.wait_answer, F.text)
async def check_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    expected_answer = data['expected_answer']

    actual_answer = message.text
    try:
        actual_answer = int(actual_answer)
    except ValueError:
        await message.answer('Please type a valid integer number')
        return

    if actual_answer != expected_answer:
        await message.answer('Incorrect answer, try again')
        return

    await message.answer('Correct! Nice job!')
    await ask_math_question(message, state)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
