import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

async def parse_to212_schedule():
    """Парсим расписание ТОЛЬКО для группы ТО-212"""
    try:
        url = "https://xn--80a3ae8b.xn--j1al4b.xn--p1ai/student/raspisanie-zanyatiy/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Получаем текущий день недели
        days_ru = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
        today_ru = days_ru[datetime.now().weekday()]
        
        # Ищем расписание для ТО-212
        content = soup.get_text()
        
        schedule_text = f"📅 *ТО-212 - Расписание на {today_ru.capitalize()}*\n\n"
        
        # Если нашли группу ТО-212 - парсим её расписание
        if 'то-212' in content.lower():
            # ВАЖНО: Нужно адаптировать под реальную структуру сайта!
            # Это временный пример - замените на реальный парсинг
            
            schedule_text += "*📍 Основное расписание:*\n"
            schedule_text += "1. Разговоры о важном | 326 | 3 корпус\n"
            schedule_text += "2. История | 323 | 3 корпус\n" 
            schedule_text += "3. Инженер. графика | 315 | 1 корпус\n"
            schedule_text += "4. Электротехника | 413 | 1 корпус\n\n"
            
            schedule_text += "*👥 Преподаватели:*\n"
            schedule_text += "• Гоменюк Д.Д. (Разговоры о важном)\n"
            schedule_text += "• Морева Е.К. (История)\n"
            schedule_text += "• Чаплина С.М. (Инженер. графика)\n"
            schedule_text += "• Румянцева М.А. (Электротехника)\n\n"
            
        else:
            # Если не нашли - показываем базовое
            schedule_text += "⚠️ *Не удалось найти расписание ТО-212*\n\n"
            schedule_text += "*Проверьте на сайте:*\n"
            schedule_text += "• Актуальность расписания\n"
            schedule_text += "• Наличие группы ТО-212\n"
            schedule_text += "• Корректность даты\n\n"
        
        # Добавляем звонки
        schedule_text += "🔔 *Расписание звонков:*\n"
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
        logger.error(f"Ошибка парсинга ТО-212: {e}")
        return "❌ Ошибка загрузки расписания ТО-212"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['📅 ТО-212 Расписание', '🔔 Звонки'],
        ['🔄 Обновить', '🌐 Сайт ТО-212']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"👋 *Бот расписания группы ТО-212*\n\n"
        f"📅 Сегодня: {datetime.now().strftime('%d.%m.%Y')}\n"
        f"🏫 МГТУ ГА\n\n"
        f"Выберите действие:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_to212_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Загружаю расписание ТО-212...")
    schedule_text = await parse_to212_schedule()
    await update.message.reply_text(schedule_text, parse_mode='Markdown')

async def show_bells(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bells_text = (
        "🔔 *Расписание звонков ТО-212:*\n\n"
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
    await update.message.reply_text("🔄 Обновляю расписание ТО-212...")
    await show_to212_schedule(update, context)

async def website_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 *Официальный сайт для ТО-212:*\n"
        "https://мгтуга.рус/student/raspisanie-zanyatiy/\n\n"
        "📍 *Группа:* ТО-212\n"
        "🏫 *Корпуса:* 1, 2, 3, 5, 6\n\n"
        "Там всегда актуальное расписание!",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if 'то-212' in text or 'расписание' in text or '📅' in text:
        await show_to212_schedule(update, context)
    elif 'звонки' in text or '🔔' in text:
        await show_bells(update, context)
    elif 'обновить' in text or '🔄' in text:
        await update_command(update, context)
    elif 'сайт' in text or '🌐' in text:
        await website_info(update, context)
    else:
        await update.message.reply_text(
            "Используйте кнопки для просмотра расписания ТО-212 👆\n\n"
            "📍 *Группа:* ТО-212\n"
            "🏫 *Корпуса:* 1, 2, 3, 5, 6",
            parse_mode='Markdown'
        )

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен для группы ТО-212!")
    application.run_polling()

if __name__ == '__main__':
    main()
