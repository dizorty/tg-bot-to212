import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

def start(update: Update, context: CallbackContext):
    keyboard = [['📅 Расписание', '🔄 Обновить'], ['❓ Помощь']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("👋 Привет! Я бот расписания ТО-212", reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("📋 Команды:\n/start - начать\n/raspisanie - расписание\n/update - обновить")

def schedule_command(update: Update, context: CallbackContext):
    schedule_text = (
        "📅 *ТО-212 - Расписание*\n\n"
        "1. *Разговоры о важном* | 326\n"
        "   👤 Гоменюк Д.Д. | 3 корпус\n\n"
        "2. *История* | 323\n"
        "   👤 Морева Е.К. | 3 корпус\n\n"
        "3. *Инженер. графика* | 315\n"
        "   👤 Чаплина С.М. | 1 корпус\n\n"
        "4. *Электротехника* | 413\n"
        "   👤 Румянцева М.А. | 1 корпус\n\n"
        "🔔 *ЗВОНКИ*\n"
        "1 пара: 08:00 - 08:55\n"
        "2 пара: 09:00-09:45 / 09:50-10:35\n\n"
        "🏢 *Корпуса:* 1, 2, 3, 5, 6\n\n"
        "🔄 *Обновлено:* 14.09.2025 23:40"
    )
    update.message.reply_text(schedule_text, parse_mode='Markdown')

def update_command(update: Update, context: CallbackContext):
    update.message.reply_text("🔄 Расписание обновлено!")
    schedule_command(update, context)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    if 'расписание' in text or '📅' in text:
        schedule_command(update, context)
    elif 'обновить' in text or '🔄' in text:
        update_command(update, context)
    elif 'помощь' in text or '❓' in text:
        help_command(update, context)
    else:
        update.message.reply_text("Используйте кнопки или /help")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("raspisanie", schedule_command))
    dp.add_handler(CommandHandler("update", update_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("✅ Бот запу
