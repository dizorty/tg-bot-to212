import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

async def parse_schedule_for_day(day_name):
    """Парсим расписание для конкретного дня"""
    try:
        # Здесь будет парсинг с сайта, пока используем заглушки
        schedule_text = f"📅 *ТО-212 - {day_name.capitalize()}*\n\n"
        
        if 'понедельник' in day_name:
            schedule_text += "1. Разговоры о важном | Гоменюк Д.Д. | 326 | 3 корпус\n"
            schedule_text += "2. История | Морева Е.К. | 323 | 3 корпус\n"
            schedule_text += "3. Инженер. графика | Чаплина С.М. | 315 | 1 корпус\n"
            schedule_text += "4. Электротехника | Румянцева М.А. | 413 | 1 корпус\n"
        elif 'вторник' in day_name:
            schedule_text += "1. Математика | 210 | 1 корпус\n"
            schedule_text += "2. Физика | 315 | 1 корпус\n"
            schedule_text += "3. Физкультура | спортзал | 2 корпус\n"
        elif 'среда' in day_name:
            schedule_text += "1. Программирование | 401 | 1 корпус\n"
            schedule_text += "2. Базы данных | 402 | 1 корпус\n"
            schedule_text += "3. Веб-разработка | 403 | 1 корпус\n"
        elif 'четверг' in day_name:
            schedule_text += "1. Иностранный язык | 205 | 2 корпус\n"
            schedule_text += "2. Экономика | 310 | 3 корпус\n"
            schedule_text += "3. Менеджмент | 312 | 3 корпус\n"
        elif 'пятница' in day_name:
            schedule_text += "1. БЖД | 115 | 1 корпус\n"
            schedule_text += "2. Экология | 116 | 1 корпус\n"
            schedule_text += "3. Проектная деятельность | 401 | 1 корпус\n"
        else:
            schedule_text += "🎉 Выходной! Пар нет\n"
        
        schedule_text += "\n🔔 *Расписание звонков:*\n"
        schedule_text += "1 пара: 08:00 - 08:55\n"
        schedule_text += "2 пара: 09:00-09:45 / 09:50-10:35\n"
        schedule_text += "3 пара: 10:50-11:35 / 11:40-12:25\n"
        schedule_text += "4 пара: 12:45-13:30 / 13:35-14:20\n"
        schedule_text += "5 пара: 14:30-15:15 / 15:20-16:05\n"
        schedule_text += "6 пара: 16:15-17:00 / 17:05-17:50\n\n"
        
        schedule_text += f"🏢 *Корпуса:* 1, 2, 3, 5, 6\n"
        schedule_text += f"🌐 *Источник:* мгтуга.рус\n"
        schedule_text += f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        
        return schedule_text
        
    except Exception as e:
        logger.error(f"Ошибка парсинга дня {day_name}: {e}")
        return f"❌ Не удалось загрузить расписание на {day_name}"

async def parse_bells_only():
    """Парсим только звонки"""
    try:
        # Парсинг звонков с сайта
        bells_text = "🔔 *Расписание звонков:*\n\n"
        bells_text += "1 пара: 08:00 - 08:55\n"
        bells_text += "2 пара: 09:00-09:45 / 09:50-10:35\n"
        bells_text += "3 пара: 10:50-11:35 / 11:40-12:25\n"
        bells_text += "4 пара: 12:45-13:30 / 13:35-14:20\n"
        bells_text += "5 пара: 14:30-15:15 / 15:20-16:05\n"
        bells_text += "6 пара: 16:15-17:00 / 17:05-17:50\n\n"
        bells_text += "🏢 *Корпуса:* 1, 2, 3, 5, 6\n"
        bells_text += f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        
        return bells_text
        
    except Exception as e:
        logger.error(f"Ошибка парсинга звонков: {e}")
        return "❌ Не удалось загрузить расписание звонков"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['📅 Понедельник', '📅 Вторник', '📅 Среда'],
        ['📅 Четверг', '📅 Пятница', '📅 Суббота'],
        ['🔔 Звонки', '🌐 Сайт', '🔄 Обновить']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "👋 *Бот расписания ТО-212*\n\n"
        "📅 Выберите день недели:\n"
        "• Понедельник - Пятница: пары\n"
        "• Суббота: выходной\n\n"
        "🏫 *Корпуса:* 1, 2, 3, 5, 6\n"
        "🌐 *Источник:* мгтуга.рус",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_day_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE, day: str):
    await update.message.reply_text(f"⏳ Загружаю расписание на {day}...")
    schedule_text = await parse_schedule_for_day(day)
    await update.message.reply_text(schedule_text, parse_mode='Markdown')

async def show_bells_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Загружаю расписание звонков...")
    bells_text = await parse_bells_only()
    await update.message.reply_text(bells_text, parse_mode='Markdown')

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Обновляю данные...")
    await start(update, context)

async def website_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 *Официальный сайт:*\n"
        "https://xn--80a3ae8b.xn--j1al4b.xn--p1ai/?date=15.09.2025&course=2&group=%D0%A2%D0%9E-212"
        "📅 *Есть выпадающий список дней*\n"
        "📍 *Группа:* ТО-212\n"
        "🏫 *Корпуса:* 1, 2, 3, 5, 6",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    days_mapping = {
        'понедельник': 'понедельник',
        'вторник': 'вторник',
        'среда': 'среда', 
        'четверг': 'четверг',
        'пятница': 'пятница',
        'суббота': 'суббота'
    }
    
    for key, day in days_mapping.items():
        if key in text:
            await show_day_schedule(update, context, day)
            return
    
    if 'звонки' in text or '🔔' in text:
        await show_bells_only(update, context)
    elif 'сайт' in text or '🌐' in text:
        await website_info(update, context)
    elif 'обнов' in text or '🔄' in text:
        await update_command(update, context)
    else:
        await update.message.reply_text("Выберите день недели 👆")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен с выбором дней!")
    application.run_polling()

if __name__ == '__main__':
    main()
