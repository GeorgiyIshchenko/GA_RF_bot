import os

from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from dotenv import load_dotenv

from handlers import *
from base_handler import QueryBot

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

application = Application.builder().token(BOT_TOKEN).build()

if __name__ == "__main__":
    application.add_handler(CommandHandler("start", start))

    # Setting up the template for department_view

    base_handler = QueryBot
    QueryBot.app = application
    QueryBot.file_path = "bot_data.json"
    QueryBot.init()

    application.add_handler(CommandHandler("departments", QueryBot.base_handler))
    application.add_handler(MessageHandler(filters.Regex("Фонды"), QueryBot.base_handler))
    application.add_handler(CallbackQueryHandler(QueryBot.base_handler, "departments"))

    # application.add_handler(CallbackQueryHandler(department_view, "\d"))

    application.add_handler(CommandHandler("rules", rules))
    application.add_handler(MessageHandler(filters.Regex("Правила"), rules))

    application.add_handler(CommandHandler("authors", authors))

    application.add_handler(MessageHandler(filters.PHOTO, photo_echo))
    application.add_handler(MessageHandler(filters.VIDEO, video_echo))

    application.run_polling()
