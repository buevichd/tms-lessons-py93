import asyncio
import logging
import os

from aiogram import Dispatcher, Bot, filters, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, any_state
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

class ConversationState(StatesGroup):
    gender = State()
    photo = State()
    location = State()
    bio = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    """Starts the conversation and asks the user about their gender."""
    await state.set_state(ConversationState.gender)
    reply_keyboard = [
        [
            KeyboardButton(text="Boy"),
            KeyboardButton(text="Girl"),
            KeyboardButton(text="Other"),
        ]
    ]
    await message.answer(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Boy or Girl?"
        ),
    )


@dp.message(ConversationState.gender, F.text.regexp(r"^(Boy|Girl|Other)$"))
async def gender(message: Message, state: FSMContext):
    """Stores the selected gender and asks for a photo."""
    user = message.from_user
    logger.info("Gender of %s: %s", user.first_name, message.text)
    await state.set_state(ConversationState.photo)
    await message.answer(
        "I see! Please send me a photo of yourself, "
        "so I know what you look like, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(ConversationState.photo, F.photo)
async def photo(message: Message, state: FSMContext):
    """Stores the photo and asks for a location."""
    user = message.from_user
    photo_file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(photo_file.file_path, "user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await state.set_state(ConversationState.location)
    await message.answer(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )


@dp.message(ConversationState.photo, Command('skip'))
async def skip_photo(message: Message, state: FSMContext):
    """Skips the photo and asks for a location."""
    user = message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await state.set_state(ConversationState.location)
    await message.answer(
        "I bet you look great! Now, send me your location please, or send /skip."
    )


@dp.message(ConversationState.location, F.location)
async def location(message: Message, state: FSMContext):
    """Stores the location and asks for some info about the user."""
    user = message.from_user
    user_location = message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await state.set_state(ConversationState.bio)
    await message.answer(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )


@dp.message(ConversationState.location, Command('skip'))
async def skip_location(message: Message, state: FSMContext):
    """Skips the location and asks for info about the user."""
    user = message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await state.set_state(ConversationState.bio)
    await message.answer(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )


@dp.message(ConversationState.bio, F.text)
async def bio(message: Message, state: FSMContext):
    """Stores the info about the user and ends the conversation."""
    user = message.from_user
    logger.info("Bio of %s: %s", user.first_name, message.text)
    await state.set_state(None)
    await message.answer("Thank you! I hope we can talk again some day.")


@dp.message(Command('cancel'))
async def cancel(message: Message, state: FSMContext):
    """Cancels and ends the conversation."""
    current_state = await state.get_state()
    if current_state is None:
        return

    user = message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await state.set_state(None)
    await message.answer(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
