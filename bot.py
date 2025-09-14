import logging
from datetime import datetime, timedelta
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

def get_schedule(day_name):
    """Возвращает расписание для указанного дня"""
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
    elif 'четверг' in day_name:
        schedule_text += "1. Иностранный язык | 205 | 2 корпус\n"
        schedule_text += "2. Экономика | 310 | 3 корпус\n"
    elif 'пятница' in day_name:
        schedule_text += "1. БЖД | 115 | 1 корпус\n"
        schedule_text += "2. Экология | 116 | 1 корпус\n"
    else:
        schedule_text += "🎉 Выходной! Пар нет\n"
    
    schedule_text += "\n🔔 *Расписание звонков:*\n"
    schedule_text += "1 пара: 08:00 - 08:55\n"
    schedule_text += "2 пара: 09:00-09:45 / 09:50-10:35\n"
    schedule_text += "3 пара: 10:50-11:35 / 11:40-12:25\n"
    schedule_text += "4 пара: 12:45-13:30 / 13:35-14:20\n"
    schedule_text += "5 пара: 14:30-15:15 / 15:20-16:05\n"
    schedule_text += "6 пара: 16:15-17:00 / 17:05-17:50\n\n"
    
    schedule_text += "🏢 *Корпуса:* 1, 2, 3, 5, 6\n"
    schedule_text += f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    
    return schedule_text

def get_bells_schedule():
    """Возвращает расписание звонков"""
    return (
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

def start(update, context):
    """Обработчик команды /start"""
    keyboard = [
        ['📅 Понедельник', '📅 Вторник', '📅 Среда'],
        ['📅 Четверг', '📅 Пятница', '📅 Суббота'],
        ['🔔 Звонки', '🌐 Сайт']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    update.message.reply_text(
        "👋 *Бот расписания ТО-212*\n\n"
        "📅 Выберите день недели:\n"
        "• Понедельник - Пятница: пары\n"
        "• Суббота: выходной\n\n"
        "🏫 *Корпуса:* 1, 2, 3, 5, 6\n"
        "🌐 *Источник:* мгтуга.рус",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def handle_message(update, context):
    """Обработчик текстовых сообщений"""
    text = update.message.text.lower()
    
    if 'понедельник' in text:
        schedule = get_schedule('понедельник')
        update.message.reply_text(schedule, parse_mode='Markdown')
    elif 'вторник' in text:
        schedule = get_schedule('вторник')
        update.message.reply_text(schedule, parse_mode='Markdown')
    elif 'среда' in text:
        schedule = get_schedule('среда')
        update.message.reply_text(schedule, parse_mode='Markdown')
    elif 'четверг' in text:
        schedule = get_schedule('четверг')
        update.message.reply_text(schedule, parse_mode='Markdown')
    elif 'пятница' in text:
        schedule = get_schedule('пятница')
        update.message.reply_text(schedule, parse_mode='Markdown')
    elif 'суббота' in text:
        schedule = get_schedule('суббота')
        update.message.reply_text(schedule, parse_mode='Markdown')
    elif 'звонки' in text:
        bells = get_bells_schedule()
        update.message.reply_text(bells, parse_mode='Markdown')
    elif 'сайт' in text:
        update.message.reply_text(
            "🌐 *Официальный сайт:*\n"
            "https://мгтуга.рус/student/raspisanie-zanyatiy/\n\n"
            "📅 *Есть выпадающий список дней*\n"
            "📍 *Группа:* ТО-212\n"
            "🏫 *Корпуса:* 1, 2, 3, 5, 6",
            parse_mode='Markdown'
        )
    else:
        update.message.reply_text("Выберите день из меню 👆")

def error(update, context):
    """Обработчик ошибок"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Основная функция"""
    logger.info("Запуск бота...")
    
    # Создаем Updater и передаем ему токен
    updater = Updater(TOKEN, use_context=True)
    
    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher
    
    # Регистрируем обработчики
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    # Регистрируем обработчик ошибок
    dp.add_error_handler(error)
    
    # Запускаем бота
    updater.start_polling()
    
    # Запускаем бота до тех пор, пока пользователь не остановит его
    logger.info("Бот запущен и готов к работе!")
    updater.idle()

if __name__ == '__main__':
    main()
