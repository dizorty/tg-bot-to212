import logging
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

async def get_schedule_for_date(date_str):
    """Получаем расписание для даты"""
    # Временные данные - позже добавим парсинг
    schedule_text = f"📅 *ТО-212 - Расписание на {date_str}*\n\n"
    
    # Стандартное расписание по дням недели
    weekday = datetime.strptime(date_str, "%d.%m.%Y").weekday()
    
    if weekday == 0:  # Понедельник
        schedule_text += "1. Разговоры о важном | Гоменюк Д.Д. | 326 | 3 корпус\n"
        schedule_text += "2. История | Морева Е.К. | 323 | 3 корпус\n"
        schedule_text += "3. Инженер. графика | Чаплина С.М. | 315 | 1 корпус\n"
        schedule_text += "4. Электротехника | Румянцева М.А. | 413 | 1 корpус\n"
    elif weekday == 1:  # Вторник
        schedule_text += "1. Математика | 210 | 1 корпус\n"
        schedule_text += "2. Физика | 315 | 1 корпус\n"
        schedule_text += "3. Физкультура | спортзал | 2 корпус\n"
    elif weekday == 2:  # Среда
        schedule_text += "1. Программирование | 401 | 1 корпус\n"
        schedule_text += "2. Базы данных | 402 | 1 корпус\n"
    elif weekday == 3:  # Четверг
        schedule_text += "1. Иностранный язык | 205 | 2 корпус\n"
        schedule_text += "2. Экономика | 310 | 3 корпус\n"
    elif weekday == 4:  # Пятница
        schedule_text += "1. БЖД | 115 | 1 корпус\n"
        schedule_text += "2. Экология | 116 | 1 корпус\n"
    else:  # Суббота/Воскресенье
        schedule_text += "🎉 Выходной! Пар нет\n"
    
    schedule_text += "\n🔔 *Расписание звонков:*\n"
    schedule_text += "1 пара: 08:00 - 08:55\n"
    schedule_text += "2 пара: 09:00-09:45 / 09:50-10:35\n"
    schedule_text += "3 пара: 10:50-11:35 / 11:40-12:25\n"
    schedule_text += "4 пара: 12:45-13:30 / 13:35-14:20\n"
    schedule_text += "5 пара: 14:30-15:15 / 15:20-16:05\n"
    schedule_text += "6 пара: 16:15-17:00 / 17:05-17:50\n\n"
    
    schedule_text += f"🏢 *Корпуса:* 1, 2, 3, 5, 6\n"
    schedule_text += f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    
    return schedule_text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['📅 Сегодня', '📅 Завтра'],
        ['📅 Понедельник', '📅 Вторник', '📅 Среда'],
        ['📅 Четверг', '📅 Пятница', '📅 Суббота'],
        ['🔔 Звонки', '🌐 Сайт']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"👋 *Бот расписания ТО-212*\n\n"
        f"📅 Выберите день:\n"
        f"• Сегодня/Завтра - актуальное расписание\n"
        f"• Дни недели - расписание по дням\n\n"
        f"🏫 *Корпуса:* 1, 2, 3, 5, 6\n"
        f"🌐 *Источник:* мгтуга.рус",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_date_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE, date_str: str):
    await update.message.reply_text(f"⏳ Загружаю расписание на {date_str}...")
    schedule_text = await get_schedule_for_date(date_str)
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
        "🌐 *Официальный сайт:*\n"
        "https://мгтуга.рус/student/raspisanie-zanyatiy/\n\n"
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
    else:
        await update.message.reply_text("Выберите опцию из меню 👆")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()
