from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

import text
import files


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(caption=text.START, photo=files.START)


async def file_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=update.message.photo[-1].file_id)
