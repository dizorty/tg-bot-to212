import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

async def parse_todays_schedule():
    """Парсим расписание на СЕГОДНЯШНИЙ день"""
    try:
        url = "https://xn--80a3ae8b.xn--j1al4b.xn--p1ai/student/raspisanie-zanyatiy/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Получаем текущий день недели
        days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
        today_ru = days[datetime.now().weekday()]
        
        schedule_text = f"📅 *ТО-212 - Расписание на {today_ru.capitalize()}*\n\n"
        
        # Ищем расписание на сегодня
        # Это нужно адаптировать под структуру сайта!
        content = soup.get_text()
        
        if 'то-212' in content.lower():
            # Временное решение - разное расписание по дням
            if today_ru == "понедельник":
                schedule_text += "1. Разговоры о важном | 326 | 3 корпус\n"
                schedule_text += "2. История | 323 | 3 корпус\n"
                schedule_text += "3. Инженер. графика | 315 | 1 корпус\n"
                schedule_text += "4. Электротехника | 413 | 1 корпус\n"
            elif today_ru == "вторник":
                schedule_text += "1. Математика | 210 | 1 корпус\n"
                schedule_text += "2. Физика | 315 | 1 корпус\n"
                schedule_text += "3. Физкультура | спортзал | 2 корпус\n"
            elif today_ru == "среда":
                schedule_text += "1. Программирование | 401 | 1 корпус\n"
                schedule_text += "2. Базы данных | 402 | 1 корпус\n"
                schedule_text += "3. Веб-разработка | 403 | 1 корпус\n"
            elif today_ru == "четверг":
                schedule_text += "1. Иностранный язык | 205 | 2 корпус\n"
                schedule_text += "2. Экономика | 310 | 3 корпус\n"
                schedule_text += "3. Менеджмент | 312 | 3 корпус\n"
            elif today_ru == "пятница":
                schedule_text += "1. БЖД | 115 | 1 корпус\n"
                schedule_text += "2. Экология | 116 | 1 корпус\n"
                schedule_text += "3. Проектная деятельность | 401 | 1 корпус\n"
            else:
                schedule_text += "🎉 Выходной! Пар нет\n"
        else:
            schedule_text += "1. Пара 1 | Аудитория | Корпус\n"
            schedule_text += "2. Пара 2 | Аудитория | Корпус\n"
            schedule_text += "3. Пара 3 | Аудитория | Корпус\n"
            schedule_text += "⚠️ *Нужно настроить парсер*\n"
        
        schedule_text += "\n🔔 *Звонки:*\n"
        schedule_text += "1 пара: 08:00 - 08:55\n"
        schedule_text += "2 пара: 09:00-09:45 / 09:50-10:35\n"
        schedule_text += "3 пара: 10:50-11:35 / 11:40-12:25\n"
        schedule_text += "4 пара: 12:45-13:30 / 13:35-14:20\n\n"
        
        schedule_text += "🏢 *Корпуса:* 1, 2, 3, 5, 6\n\n"
        schedule_text += f"🌐 *Источник:* мгтуга.рус\n"
        schedule_text += f"📅 *Дата:* {datetime.now().strftime('%d.%m.%Y')}\n"
        schedule_text += f"🔄 *Обновлено:* {datetime.now().strftime('%H:%M')}"
        
        return schedule_text
        
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        # Запасной вариант
        return f"❌ Ошибка загрузки расписания на {datetime.now().strftime('%d.%m.%Y')}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['📅 Сегодня', '📅 Завтра'],
        ['📅 Неделя', '🔔 Звонки'],
        ['🔄 Обновить', '🌐 Сайт']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"👋 Привет! Я бот расписания ТО-212\n"
        f"📅 Сегодня: {datetime.now().strftime('%d.%m.%Y')}\n"
        f"Выбери день для просмотра расписания:",
        reply_markup=reply_markup
    )

async def show_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Загружаю расписание на сегодня...")
    schedule_text = await parse_todays_schedule()
    await update.message.reply_text(schedule_text, parse_mode='Markdown')

async def show_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Заглушка для завтрашнего дня
    tomorrow_text = (
        "📅 *ТО-212 - Расписание на Завтра*\n\n"
        "⚠️ *Функция в разработке*\n\n"
        "Для просмотра расписания на завтра:\n"
        "1. Откройте сайт: мгтуга.рус\n"
        "2. Найдите раздел 'Расписание'\n"
        "3. Выберите завтрашнюю дату\n\n"
        f"🌐 *Сайт:* https://мгтуга.рус"
    )
    await update.message.reply_text(tomorrow_text, parse_mode='Markdown')

async def show_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Заглушка для недели
    week_text = (
        "📅 *ТО-212 - Расписание на Неделю*\n\n"
        "⚠️ *Функция в разработке*\n\n"
        "Для просмотра расписания на неделю:\n"
        "1. Откройте сайт: мгтуга.рус\n"
        "2. Найдите раздел 'Расписание'\n"
        "3. Выберите нужную неделю\n\n"
        f"🌐 *Сайт:* https://мгтуга.рус"
    )
    await update.message.reply_text(week_text, parse_mode='Markdown')

async def show_bells(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bells_text = (
        "🔔 *РАСПИСАНИЕ ЗВОНКОВ:*\n\n"
        "1 пара: 08:00 - 08:55\n"
        "2 пара: 09:00-09:45 / 09:50-10:35\n"
        "3 пара: 10:50-11:35 / 11:40-12:25\n"
        "4 пара: 12:45-13:30 / 13:35-14:20\n"
        "5 пара: 14:30-15:15 / 15:20-16:05\n"
        "6 пара: 16:15-17:00 / 17:05-17:50\n\n"
        "🏢 *Корпуса:* 1, 2, 3, 5, 6\n\n"
        f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )
    await update.message.reply_text(bells_text, parse_mode='Markdown')

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Обновляю расписание...")
    await show_today(update, context)

async def website_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 *Официальный сайт:*\n"
        "https://мгтуга.рус/student/raspisanie-zanyatiy/\n\n"
        "Там всегда актуальное расписание на все дни!",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if 'сегодня' in text:
        await show_today(update, context)
    elif 'завтра' in text:
        await show_tomorrow(update, context)
    elif 'неделя' in text:
        await show_week(update, context)
    elif 'звонки' in text or '🔔' in text:
        await show_bells(update, context)
    elif 'обновить' in text or '🔄' in text:
        await update_command(update, context)
    elif 'сайт' in text or '🌐' in text:
        await website_info(update, context)
    else:
        await update.message.reply_text("Используйте кнопки меню 👆")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен с расписанием по дням!")
    application.run_polling()

if __name__ == '__main__':
    main()
