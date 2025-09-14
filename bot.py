import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

def start(update, context):
    keyboard = [['📅 Расписание'], ['🔄 Обновить']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("👋 Привет! Я бот расписания ТО-212", reply_markup=reply_markup)

def schedule_command(update, context):
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
    update.message.reply_text(schedule_text, parse_mode='Markdown')

def handle_message(update, context):
    text = update.message.text.lower()
    if 'расписание' in text or '📅' in text:
        schedule_command(update, context)
    elif 'обновить' in text or '🔄' in text:
        update.message.reply_text("✅ Расписание обновлено!")
        schedule_command(update, context)
    else:
        update.message.reply_text("Используйте кнопки меню")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("raspisanie", schedule_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    print("✅ Бот запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
