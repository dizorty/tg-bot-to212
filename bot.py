import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import re
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Лучше хранить токен в переменной окружения:
# TOKEN = os.environ.get("BOT_TOKEN")
TOKEN = "8388176239:AAH2Ktp55xC0Wj10J4s86GjqLz5CcJDcCcU"

DAYS = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']

async def parse_schedule(day: str = None):
    """Парсим расписание с сайта. Если day задан — пытаемся вернуть только этот день."""
    try:
        # Читабельный (unicode) домен — requests обычно его корректно обработает
        url = "https://мгтуга.рус/student/raspisanie-zanyatiy/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }

        response = requests.get(url, headers=headers, timeout=10)
        # иногда кодировка определяется некорректно — используем apparent_encoding
        response.encoding = response.apparent_encoding or 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Собираем весь текст страницы в удобном виде
        page_text = soup.get_text(separator="\n")
        # Очищаем пустые строки и лишние пробелы
        lines = [ln.strip() for ln in page_text.splitlines() if ln.strip()]
        page_text = "\n".join(lines)

        # Пытаемся найти блоки по заголовкам дней (если они есть на странице)
        pattern = r'(?P<day>' + '|'.join(DAYS) + r')(?P<block>.*?)(?=(?:' + '|'.join(DAYS) + r')|$)'
        matches = re.finditer(pattern, page_text, flags=re.DOTALL | re.IGNORECASE)
        day_blocks = {}
        for m in matches:
            key = m.group('day').strip().lower().capitalize()
            block = m.group('block').strip()
            # Небольшая фильтрация: отрезаем очень длинные блоки, если нужно — можно улучшить
            day_blocks[key] = block

        header = "📅 *ТО-212 - Расписание*\n\n"
        footer = f"🏢 *Корпуса:* 1, 2, 3, 5, 6\n🌐 *Источник:* мгтуга.рус\n🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"

        if day:
            day_cap = day.capitalize()
            if day_blocks.get(day_cap):
                schedule_text = header + f"*{day_cap}*\n{day_blocks[day_cap]}\n\n" + footer
                return schedule_text
            else:
                # Если на сайте нет разбивки по дням — вернем общее расписание (фоллбек)
                logger.info(f"Данные для {day_cap} не найдены на странице — показываю общее расписание.")
                # fallback — ваш статичный шаблон (можно заменить на любой другой)
                schedule_text = header
                schedule_text += "1. Разговоры о важном | Гоменюк Д.Д. | 326 | 3 корпус\n"
                schedule_text += "2. История | Морева Е.К. | 323 | 3 корпус\n"
                schedule_text += "3. Инженер. графика | Чаплина С.М. | 315 | 1 корпус\n"
                schedule_text += "4. Электротехника | Румянцева М.А. | 413 | 1 корпус\n\n"
                schedule_text += "🔔 *Расписание звонков:*\n"
                schedule_text += "1 пара: 08:00 - 08:55\n"
                schedule_text += "2 пара: 09:00-09:45 / 09:50-10:35\n"
                schedule_text += "3 пара: 10:50-11:35 / 11:40-12:25\n"
                schedule_text += "4 пара: 12:45-13:30 / 13:35-14:20\n"
                schedule_text += "5 пара: 14:30-15:15 / 15:20-16:05\n"
                schedule_text += "6 пара: 16:15-17:00 / 17:05-17:50\n\n"
                schedule_text += footer
                return schedule_text

        # Если day не указан — пытаемся вернуть всё, что нашли по дням.
        schedule_text = header
        if day_blocks:
            for d in DAYS:
                if d in day_blocks:
                    schedule_text += f"*{d}*\n{day_blocks[d]}\n\n"
        else:
            # Фоллбек — тот же статичный шаблон
            schedule_text += "1. Разговоры о важном | Гоменюк Д.Д. | 326 | 3 корпус\n"
            schedule_text += "2. История | Морева Е.К. | 323 | 3 корпус\n"
            schedule_text += "3. Инженер. графика | Чаплина С.М. | 315 | 1 корпус\n"
            schedule_text += "4. Электротехника | Румянцева М.А. | 413 | 1 корпус\n\n"
            schedule_text += "🔔 *Расписание звонков:*\n"
            schedule_text += "1 пара: 08:00 - 08:55\n"
            schedule_text += "2 пара: 09:00-09:45 / 09:50-10:35\n"
            schedule_text += "3 пара: 10:50-11:35 / 11:40-12:25\n"
            schedule_text += "4 пара: 12:45-13:30 / 13:35-14:20\n"
            schedule_text += "5 пара: 14:30-15:15 / 15:20-16:05\n"
            schedule_text += "6 пара: 16:15-17:00 / 17:05-17:50\n\n"

        schedule_text += footer
        return schedule_text

    except Exception as e:
        logger.error(f"Ошибка парсинга расписания: {e}")
        return "❌ Не удалось загрузить расписание. Попробуйте позже."

async def parse_bells_only():
    """Парсим только звонки (статично, можно вынести из сайта если нужно)."""
    try:
        bells_text = "🔔 *Расписание звонков:*\n\n"
        bells_text += "1 пара: 08:00 - 08:55\n"
        bells_text += "2 пара: 09:00-09:45 / 09:50-10:35\n"
        bells_text += "3 пара: 10:50-11:35 / 11:40-12:25\n"
        bells_text += "4 пара: 12:45-13:30 / 13:35-14:20\n"
        bells_text += "5 пара: 14:30-15:15 / 15:20-16:05\n"
        bells_text += "6 пара: 16:15-17:00 / 17:05-17:50\n\n"
        bells_text += "🏢 *Корпуса:* 1, 2, 3, 5, 6\n"
        bells_text += f"🌐 *Источник:* мгтуга.рус\n"
        bells_text += f"🔄 *Обновлено:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        return bells_text
    except Exception as e:
        logger.error(f"Ошибка парсинга звонков: {e}")
        return "❌ Не удалось загрузить расписание звонков. Попробуйте позже."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['📅 Полное расписание', '🔔 Только звонки'],
        ['Понедельник', 'Вторник', 'Среда'],
        ['Четверг', 'Пятница', 'Суббота'],
        ['Воскресенье', '🔄 Обновить', '🌐 Сайт'],
        ['❓ Помощь']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Привет! Я бот расписания ТО-212\n"
        "Выбери день недели или команду:",
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
        "• Выберите день недели - показать расписание конкретного дня\n"
        "• Обновить - перезагрузить с сайта\n"
        "• Сайт - ссылка на источник\n"
        "• Помощь - эта справка",
        parse_mode='Markdown'
    )

def normalize_day_input(text: str):
    t = text.strip().lower()
    map_short = {
        'пн':'Понедельник','вт':'Вторник','ср':'Среда','чт':'Четверг','пт':'Пятница','сб':'Суббота','вс':'Воскресенье'
    }
    if t in map_short:
        return map_short[t]
    # полные названия
    for d in DAYS:
        if t == d.lower():
            return d
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    # Проверим дни недели в явном виде
    day = normalize_day_input(text)
    if day:
        await update.message.reply_text(f"⏳ Загружаю расписание на {day}...")
        schedule_text = await parse_schedule(day=day)
        await update.message.reply_text(schedule_text, parse_mode='Markdown')
        return

    if 'полное расписание' in text or '📅' in text:
        await show_full_schedule(update, context)
    elif 'только звонки' in text or '🔔' in text:
        await show_bells_only(update, context)
    elif 'обновить' in text or '🔄' in text:
        await update_command(update, context)
    elif 'сайт' in text or '🌐' in text:
        await website_info(update, context)
    elif 'помощь' in text or '❓' in text:
        await help_command(update, context)
    else:
        await update.message.reply_text("Выберите опцию из меню 👆 или нажмите нужный день недели.")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()
