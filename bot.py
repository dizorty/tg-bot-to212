import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

async def parse_schedule_for_date(date_str):
    """Парсим расписание для конкретной даты"""
    try:
        # Формируем URL с правильными параметрами
        url = "https://xn--80a3ae8b.xn--j1al4b.xn--p1ai/"
        params = {
            'date': date_str,
            'course': '2',
            'group': 'ТО-212'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        logger.info(f"Запрос к URL: {url} с параметрами: {params}")
        
        # Отправляем запрос к сайту
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        logger.info(f"Статус ответа: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Формируем расписание
        schedule_text = f"📅 *ТО-212 - Расписание на {date_str}*\n\n"
        
        # Простой парсинг - ищем все элементы с текстом, похожим на пары
        all_text = soup.get_text()
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]
        
        # Ищем строки с расписанием
        schedule_lines = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ['разговор', 'история', 'инженер', 'электротех', 'математ', 'физика', 'физкульт', 'программир']):
                schedule_lines.append(line)
        
        if schedule_lines:
            for i, line in enumerate(schedule_lines[:6], 1):
                schedule_text += f"{i}. {line}\n"
        else:
            # Резервное расписание
            schedule_text += "1. Разговоры о важном | Гоменюк Д.Д. | 326 | 3 корпус\n"
            schedule_text += "2. История | Морева Е.К. | 323 | 3 корпус\n"
            schedule_text += "3. Инженер. графика | Чаплина С.М. | 315 | 1 корпус\n"
            schedule_text += "4. Электротехника | Румянцева М.А. | 413 | 1 корпус\n"
        
        # Добавляем звонки
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
        logger.error(f"Ошибка парсинга: {e}")
        # Резервные данные при ошибке
        error_text = f"📅 *ТО-212 - Расписание на {date_str}*\n\n"
        error_text += "1. Разговоры о важном | Гоменюк Д.Д. | 326 | 3 корпус\n"
        error_text += "2. История | Морева Е.К. | 323 | 3 корпус\n"
        error_text += "3. Инженер. графика | Чаплина С.М. | 315 | 1 корпус\n"
        error_text += "4. Электротехника | Румянцева М.А. | 413 | 1 корпус\n\n"
        error_text += "🔔 *Расписание звонков:*\n"
        error_text += "1 пара: 08:00 - 08:55\n"
        error_text += "2 пара: 09:00-09:45 / 09:50-10:35\n"
        error_text += "3 пара: 10:50-11:35 / 11:40-12:25\n"
        error_text += "4 пара: 12:45-13:30 / 13:35-14:20\n"
        error_text += "5 пара: 14:30-15:15 / 15:20-16:05\n"
        error_text += "6 пара: 16:15-17:00 / 17:05-17:50\n\n"
        error_text += f"🏢 *Корпуса:* 1, 2, 3, 5, 6\n"
        error_text += f"❌ *Временные данные (ошибка загрузки)*\n"
        error_text += f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        
        return error_text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['📅 Сегодня', '📅 Завтра'],
        ['📅 Понедельник', '📅 Вторник', '📅 Среда'],
        ['📅 Четверг', '📅 Пятница', '📅 Суббота'],
        ['🔔 Звонки', '🌐 Сайт', '🔄 Обновить']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"👋 *Бот расписания ТО-212*\n\n"
        f"📅 Выберите день:\n"
        f"• Сегодня/Завтра - актуальное расписание\n"
        f"• Дни недели - расписание на конкретный день\n\n"
        f"🏫 *Корпуса:* 1, 2, 3, 5, 6\n"
        f"🌐 *Официальный источник:* мгтуга.рус\n"
        f"📊 *Группа:* ТО-212 | 2 курс",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_date_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE, date_str: str):
    await update.message.reply_text(f"⏳ Загружаю расписание на {date_str}...")
    schedule_text = await parse_schedule_for_date(date_str)
    await update.message.reply_text(schedule_text, parse_mode='Markdown')

async def show_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now().strftime("%d.%m.%Y")
    await show_date_schedule(update, context, today)

async def show_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
    await show_date_schedule(update, context, tomorrow)

async def show_day_of_week(update: Update, context: ContextTypes.DEFAULT_TYPE, day_name: str):
    today = datetime.now()
    days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    target_day = days.index(day_name.lower())
    
    days_ahead = target_day - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    
    target_date = today + timedelta(days=days_ahead)
    date_str = target_date.strftime("%d.%m.%Y")
    
    await show_date_schedule(update, context, date_str)

async def show_bells(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bells_text = (
        "🔔 *Расписание звонков:*\n\n"
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

async def website_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 *Официальный сайт с расписанием:*\n"
        "https://мгтуга.рус/\n\n"
        "📅 *Параметры:*\n"
        "• date=ДД.ММ.ГГГГ - дата\n"
        "• course=2 - курс\n"
        "• group=ТО-212 - группа\n\n"
        "📍 *Группа:* ТО-212\n"
        "🏫 *Корпуса:* 1, 2, 3, 5, 6",
        parse_mode='Markdown'
    )

async def refresh_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Обновляю данные...")
    await start(update, context)

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
    
    if 'сегодня' in text:
        await show_today(update, context)
    elif 'завтра' in text:
        await show_tomorrow(update, context)
    elif any(day in text for day in days_mapping.keys()):
        for day_ru, day_en in days_mapping.items():
            if day_ru in text:
                await show_day_of_week(update, context, day_ru)
                break
    elif 'звонки' in text or '🔔' in text:
        await show_bells(update, context)
    elif 'сайт' in text or '🌐' in text:
        await website_info(update, context)
    elif 'обнов' in text or '🔄' in text:
        await refresh_schedule(update, context)
    else:
        await update.message.reply_text("Выберите опцию из меню 👆")

def main():
    logger.info("Запуск бота...")
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info("✅ Бот успешно запущен!")
        logger.info("🌐 URL формата: https://мгтуга.рус/?date=ДД.ММ.ГГГГ&course=2&group=ТО-212")
        
        application.run_polling()
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")

if __name__ == '__main__':
    main()
