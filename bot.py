import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['📅 Расписание'], ['🔄 Обновить']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Привет! Я бот расписания ТО-212", reply_markup=reply_markup)

async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    schedule_text = (
        "📅 *ТО-212 - Расписание*\n\n"
        "1. Разговоры о важном | 326\n"
        "   👤 Гоменюк Д.Д. | 3 корпус\n\n"
        "2. История | 323\n"
        "   👤 Морева Е.К. | 3 корпус\n\n"
        "3. Инженер. графика | 315\n"
        "   👤 Чаплина С.М. | 1 корпус\n\n"
        "4. Электротехника | 413\n"
        "   👤 Румянцева М.А. | 1 корпус\n\n"
        "🔔 *ЗВОНКИ*\n"
        "1 пара: 08:00 - 08:55\n"
        "2 пара: 09:00-09:45 / 09:50-10:35\n\n"
        "🏢 *Корпуса:* 1, 2, 3, 5, 6"
    )
    await update.message.reply_text(schedule_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if 'расписание' in text or '📅' in text:
        await schedule_command(update, context)
    elif 'обновить' in text or '🔄' in text:
        await update.message.reply_text("✅ Расписание обновлено!")
        await schedule_command(update, context)
    else:
        await update.message.reply_text("Используйте кнопки меню")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("raspisanie", schedule_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()
