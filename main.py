import os
import logging

from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from dotenv import load_dotenv

from handlers import *
from base_handler import QueryBot

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

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
    application.add_handler(MessageHandler(filters.Document.ALL, doc_echo))

    application.run_polling()
