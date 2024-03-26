import asyncio
import logging
import random
import sys
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, \
    InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.markdown import hbold

from lesson_40.polls_models import Database, Question, Choice

TOKEN = getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
database = Database()


async def ask_random_question(message: Message):
    questions: list[Question] = database.get_questions()
    assert len(questions) > 0
    question: Question = questions[random.randint(0, len(questions) - 1)]
    keyboard = [
        [InlineKeyboardButton(text=choice.choice_text,
                              callback_data=f'question_id:{question.id}:choice_id:{choice.id}')]
        for choice in question.choices]
    await message.answer(question.question_text,
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))


def generate_choice_message(choice: Choice, selected_choice: Choice):
    return f'{choice.choice_text}' + \
        (hbold(' (selected)') if choice.id == selected_choice.id else '') + \
        f' - {choice.votes}'


def generate_question_statistics_message(question: Question, selected_choice: Choice) -> str:
    return f'Question: {question.question_text}\n' + \
        f'Choices:\n' + \
        '\n'.join(
            f' * {generate_choice_message(choice, selected_choice)}'
            for choice in question.choices)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Hello, I'm polls bot!")
    await ask_random_question(message)


@dp.callback_query(F.data.regexp(r'^question_id:(\d+):choice_id:(\d+)$'))
async def answer_handler(callback: CallbackQuery):
    data = callback.data.split(':')
    question_id = int(data[1])
    choice_id = int(data[3])
    await callback.message.edit_reply_markup(reply_markup=None)

    question = database.get_question(question_id)
    selected_choice = [choice for choice in question.choices if choice.id == choice_id][0]

    selected_choice.votes += 1

    message_text = generate_question_statistics_message(question, selected_choice)
    await callback.message.answer(message_text)
    await ask_random_question(callback.message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
