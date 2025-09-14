import os
import logging
import asyncio
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"
current_schedule = None

async def fetch_schedule():
    global current_schedule
    try:
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
            f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )
        current_schedule = schedule_text
        logger.info("Расписание обновлено")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        current_schedule = "❌ Ошибка загрузки расписания"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['📅 Расписание', '🔄 Обновить'], ['❓ Помощь']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Привет! Я бот расписания ТО-212", reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Команды:\n/start - начать\n/raspisanie - расписание\n/update - обновить")

async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if current_schedule is None:
        await update.message.reply_text("⏳ Загружаю...")
        await fetch_schedule()
    await update.message.reply_text(current_schedule, parse_mode='Markdown')

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Обновляю...")
    await fetch_schedule()
    await update.message.reply_text(current_schedule, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if 'расписание' in text or '📅' in text:
        await schedule_command(update, context)
    elif 'обновить' in text or '🔄' in text:
        await update_command(update, context)
    elif 'помощь' in text or '❓' in text:
        await help_command(update, context)
    else:
        await update.message.reply_text("Используйте кнопки или /help")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("raspisanie", schedule_command))
    application.add_handler(CommandHandler("update", update_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен на Render!")
    application.run_polling()

if __name__ == '__main__':
    asyncio.run(fetch_schedule())
    main()
