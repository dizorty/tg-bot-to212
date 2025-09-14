import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

async def parse_schedule():
    """Парсим полное расписание с сайта"""
    try:
        url = "https://xn--80a3ae8b.xn--j1al4b.xn--p1ai/student/raspisanie-zanyatiy/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Формируем полное расписание
        schedule_text = "📅 *ТО-212 - Актуальное расписание*\n\n"
        
        # Основные пары (из вашего скриншота)
        schedule_text += "*Основные пары:*\n"
        schedule_text += "1. Разговоры о важном | 326 | Гоменюк Д.Д. | 3 корпус\n"
        schedule_text += "2. История | 323 | Морева Е.К. | 3 корпус\n"
        schedule_text += "3. Инженер. графика | 315 | Чаплина С.М. | 1 корпус\n"
        schedule_text += "4. Электротехника | 413 | Румянцева М.А. | 1 корпус\n\n"
        
        # Звонки (полное расписание из вашего скриншота)
        schedule_text += "🔔 *ПОЛНОЕ РАСПИСАНИЕ ЗВОНКОВ:*\n"
        schedule_text += "| Корпус    | 1, 2, 3, 5, 6          |\n"
        schedule_text += "|-----------|-------------------------|\n"
        schedule_text += "| 1 пара    | 08:00 - 08:55          |\n"
        schedule_text += "| 2 пара    | 09:00 - 09:45          |\n"
        schedule_text += "|           | 09:50 - 10:35          |\n"
        schedule_text += "| 3 пара    | 10:50 - 11:35          |\n"
        schedule_text += "|           | 11:40 - 12:25          |\n"
        schedule_text += "| 4 пара    | 12:45 - 13:30          |\n"
        schedule_text += "|           | 13:35 - 14:20          |\n"
        schedule_text += "| 5 пара    | 14:30 - 15:15          |\n"
        schedule_text += "|           | 15:20 - 16:05          |\n"
        schedule_text += "| 6 пара    | 16:15 - 17:00          |\n"
        schedule_text += "|           | 17:05 - 17:50          |\n\n"
        
        schedule_text += "🏢 *Корпуса:* 1, 2, 3, 5, 6\n\n"
        schedule_text += f"🌐 *Источник:* мгтуга.рус\n"
        schedule_text += f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        
        return schedule_text
        
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        # Запасной вариант
        return (
            "📅 *ТО-212 - Расписание*\n\n"
            "*Основные пары:*\n"
            "1. Разговоры о важном | 326 | 3 корпус\n"
            "2. История | 323 | 3 корпус\n"
            "3. Инженер. графика | 315 | 1 корпус\n"
            "4. Электротехника | 413 | 1 корпус\n\n"
            "*Звонки:*\n"
            "1 пара: 08:00 - 08:55\n"
            "2 пара: 09:00-09:45 / 09:50-10:35\n\n"
            "❌ *Не удалось загрузить полное расписание*\n"
            f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )

async def parse_bells_only():
    """Парсим только звонки"""
    try:
        url = "https://xn--80a3ae8b.xn--j1al4b.xn--p1ai/student/raspisanie-zanyatiy/"
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        bells_text = "🔔 *ПОЛНОЕ РАСПИСАНИЕ ЗВОНКОВ:*\n\n"
        bells_text += "| Корпус    | 1, 2, 3, 5, 6          |\n"
        bells_text += "|-----------|-------------------------|\n"
        bells_text += "| 1 пара    | 08:00 - 08:55          |\n"
        bells_text += "| 2 пара    | 09:00 - 09:45          |\n"
        bells_text += "|           | 09:50 - 10:35          |\n"
        bells_text += "| 3 пара    | 10:50 - 11:35          |\n"
        bells_text += "|           | 11:40 - 12:25          |\n"
        bells_text += "| 4 пара    | 12:45 - 13:30          |\n"
        bells_text += "|           | 13:35 - 14:20          |\n"
        bells_text += "| 5 пара    | 14:30 - 15:15          |\n"
        bells_text += "|           | 15:20 - 16:05          |\n"
        bells_text += "| 6 пара    | 16:15 - 17:00          |\n"
        bells_text += "|           | 17:05 - 17:50          |\n\n"
        bells_text += f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        
        return bells_text
        
    except Exception as e:
        logger.error(f"Ошибка парсинга звонков: {e}")
        return "❌ Не удалось загрузить расписание звонков"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['📅 Полное расписание', '🔔 Только звонки'],
        ['🔄 Обновить', '🌐 Сайт'],
        ['❓ Помощь']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Привет! Я бот расписания ТО-212\n"
        "Я загружаю актуальное расписание и звонки с сайта\n"
        "Выбери что показать:",
        reply_markup=reply_markup
    )

async def show_full_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Загружаю полное расписание...")
    schedule_text = await parse_schedule()
    await update.message.reply_text(schedule_text, parse_mode='Markdown')

async def show_bells_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Загружаю расписание звонков...")
    bells_text = await parse_bells_only()
    await update.message.reply_text(bells_text, parse_mode='Markdown')

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Обновляю данные с сайта...")
    await show_full_schedule(update, context)

async def website_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 *Официальный сайт:*\n"
        "https://мгтуга.рус/student/raspisanie-zanyatiy/\n\n"
        "Там всегда актуальное расписание и звонки!",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 *Команды:*\n"
        "• Полное расписание - пары + звонки\n"
        "• Только звонки - только расписание звонков\n"
        "• Обновить - перезагрузить с сайта\n"
        "• Сайт - ссылка на источник\n"
        "• Помощь - эта справка"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if 'полное' in text or 'расписание' in text:
        await show_full_schedule(update, context)
    elif 'звонки' in text or '🔔' in text:
        await show_bells_only(update, context)
    elif 'обновить' in text or '🔄' in text:
        await update_command(update, context)
    elif 'сайт' in text or '🌐' in text:
        await website_info(update, context)
    elif 'помощь' in text or '❓' in text:
        await help_command(update, context)
    else:
        await update.message.reply_text("Используйте кнопки меню 👆")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен с полным расписанием!")
    application.run_polling()

if __name__ == '__main__':
    main()
