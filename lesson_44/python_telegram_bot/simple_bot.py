import os
from telegram import Update
from telegram.ext import CallbackContext, ApplicationBuilder, CommandHandler

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(f'Hello {update.effective_user.full_name}!')

if __name__ == '__main__':
    token = os.environ['TELEGRAM_BOT_TOKEN']
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.run_polling()
