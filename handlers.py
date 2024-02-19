from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

import text
import files

from department import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Фонды"), KeyboardButton(text="Правила")]],
        one_time_keyboard=True,
        input_field_placeholder="Перед изучением фондов рекомендуется ознакомиться с правилами."
    )
    await update.message.reply_photo(caption=text.START, photo=files.START, reply_markup=reply_markup)


async def departments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer("Список фондов")
        message = query.message
    else:
        message = update.message

    keyboard = list()
    for item in departments_dict.items():
        i, department = item
        keyboard.append([InlineKeyboardButton(text=department.name, callback_data=f"{i}")])

    await message.reply_photo(caption=text.DEPARTMENTS, photo=files.DEPARTMENT,
                              reply_markup=InlineKeyboardMarkup(keyboard))


async def department_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    department: Department = departments_dict.get(int(query.data))

    keyboard = list()
    keyboard.append([InlineKeyboardButton(text="🗺 Путеводитель", url=department.guide_url)])
    keyboard.append([InlineKeyboardButton(text="‼️ Условия ознакомления с материалами", url=department.rules_url)])
    keyboard.append([InlineKeyboardButton(text="🚶‍♂️ Назад", callback_data="departments")])

    await query.message.reply_video(video=department.video_url, caption=str(department),
                                    reply_markup=InlineKeyboardMarkup(keyboard), supports_streaming=True)


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(caption=text.RULES, photo=files.RULES)


async def authors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=text.AUTHORS)


async def photo_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=update.message.photo[-1].file_id)


async def video_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=update.message.video.file_id)
