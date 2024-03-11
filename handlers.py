from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, \
    ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes, ConversationHandler

import text
import files

from department import *

FIRST, SECOND, THIRD = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_video_note(video_note=files.START_VIDEO_NOTE)
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Пройти опрос")],
                  [KeyboardButton(text="Фонды"), KeyboardButton(text="Правила")]],
        one_time_keyboard=True,
        input_field_placeholder="Перед изучением фондов рекомендуется пройти опрос."
    )
    await update.message.reply_text(text=text.START, reply_markup=reply_markup)

    return FIRST


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


async def doc_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=update.message.document.file_id)


async def video_note_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=update.message.video_note.file_id)


async def web_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Web App", reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="WebApp", web_app=WebAppInfo("D:/Projects/fullmotion/index.html"))]]))


async def initial_q(update: Update, context: ContextTypes):
    await update.message.reply_text(text="❓ Что вы знаете о человеке?", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton(text="Был репрессирован")],
        [KeyboardButton(text="Участвовал в ВОВ")]
    ]))

    return SECOND


async def repression_q(update: Update, context: ContextTypes):
    await update.message.reply_text(text="Вам подойдет фонд \"Репрессии\"")
    return ConversationHandler.END


async def vov_q(update: Update, context: ContextTypes):
    await update.message.reply_text(text="Вам подойдет фонд \"ВОВ\"")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Пока! Надеюсь, ", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
