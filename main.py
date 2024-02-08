import os

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from dotenv import load_dotenv

from handlers import *

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

application = Application.builder().token(BOT_TOKEN).build()

if __name__ == "__main__":
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, file_echo))

    application.run_polling()
