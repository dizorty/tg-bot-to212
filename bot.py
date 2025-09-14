import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

# Расписание на разные дни
schedule_data = {
    "понедельник": [
        "1. Разговоры о важном | 326 | Гоменюк Д.Д. | 3 корпус",
        "2. История | 323 | Морева Е.К. | 3 корпус", 
        "3. Инженер. графика | 315 | Чаплина С.М. | 1 корпус",
        "4. Электротехника | 413 | Румянцева М.А. | 1 корпус"
    ],
    "вторник": [
        "1. Математика | 210 | Петров И.И. | 1 корпус",
        "2. Физика | 315 | Сидоров А.А. | 1 корпус",
        "3. Физкультура | спортзал | Кузнецов С.С. | 2 корпус"
    ],
    "среда": [
        "1. Программирование | 401 | Иванова О.П. | 1 корпус",
        "2. Базы данных | 402 | Смирнов Д.В. | 1 корпус",
        "3. Веб-разработка | 403 | Козлов М.И. | 1 корпус"
    ],
    "четверг": [
        "1. Иностранный язык | 205 | Johnson M. | 2 корпус",
        "2. Экономика | 310 | Васильева Л.К. | 3 корпус",
        "3. Менеджмент | 312 | Попов Н.Н. | 3 корпус"
    ],
    "пятница": [
        "1. БЖД | 115 | Орлов С.П. | 1 корпус",
        "2. Экология | 116 | Зеленая Е.В. | 1 корпус",
        "3. Проектная деятельность | 401 | руководитель"
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['📅 Понедельник', '📅 Вторник'],
        ['📅 Среда', '📅 Четверг'], 
        ['📅 Пятница', '📅 Сегодня'],
        ['🔄 Обновить']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Привет! Я бот расписания ТО-212\n"
        "Выбери день недели или нажми 'Сегодня'",
        reply_markup=reply_markup
    )

async def show_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE, day: str):
    if day in schedule_data:
        schedule_text = f"📅 *Расписание на {day.capitalize()}*\n\n"
        for lesson in schedule_data[day]:
            schedule_text += f"• {lesson}\n"
        
        schedule_text += "\n🔔 *ЗВОНКИ*\n"
        schedule_text += "1 пара: 08:00 - 08:55\n"
        schedule_text += "2 пара: 09:00-09:45 / 09:50-10:35\n\n"
        schedule_text += "🏢 *Корпуса:* 1, 2, 3, 5, 6\n\n"
        schedule_text += f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        
        await update.message.reply_text(schedule_text, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Расписание на этот день не найдено")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    days = {
        'понедельник': 'понедельник',
        'вторник': 'вторник', 
        'среда': 'среда',
        'четверг': 'четверг',
        'пятница': 'пятница',
        'сегодня': datetime.now().strftime('%A').lower()
    }
    
    for day_key, day_value in days.items():
        if day_key in text:
            await show_schedule(update, context, day_value)
            return
    
    if 'обновить' in text or '🔄' in text:
        await update.message.reply_text("✅ Расписание обновлено!")
        await start(update, context)
    else:
        await update.message.reply_text("Выбери день недели на клавиатуре 👆")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()
