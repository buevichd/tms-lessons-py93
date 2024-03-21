import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

async def start(update: Update, context: CallbackContext):
    await update.message.reply_html(rf"Hi {update.effective_user.mention_html()}!")

async def help(update: Update, context: CallbackContext):
    await update.message.reply_html("There should be help message")

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

if __name__ == "__main__":
    application = Application.builder().token(os.environ['TELEGRAM_BOT_TOKEN']).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


