from datetime import datetime
import telebot
import requests
import os
import re
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
SHEET_URL = os.getenv("SHEET_BEST_URL")

# Инициализация Telegram-бота
bot = telebot.TeleBot(TOKEN)

# Временное хранилище данных пользователей
user_data = {}

# Обработка команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Напиши своё имя:")
    user_data[message.chat.id] = {}

# Получение имени
@bot.message_handler(func=lambda message: message.chat.id in user_data and 'name' not in user_data[message.chat.id])
def handle_name(message):
    user_data[message.chat.id]['name'] = message.text.strip()
    bot.send_message(message.chat.id, "Теперь укажи номер телефона в международном формате (например, +4915123456789):")

# Получение телефона с валидацией
@bot.message_handler(func=lambda message: 'name' in user_data[message.chat.id] and 'phone' not in user_data[message.chat.id])
def handle_phone(message):
    phone = message.text.strip()
    # Проверка на международный формат: + и 10–15 цифр
    if re.match(r'^\+\d{10,15}$', phone):
        user_data[message.chat.id]['phone'] = phone
        bot.send_message(message.chat.id, "Отлично! Опиши услугу, которая тебе интересна:")
    else:
        bot.send_message(message.chat.id, "❌ Неверный формат. Попробуй снова в виде: +4915123456789")

# Получение услуги и отправка заявки
@bot.message_handler(func=lambda message: 'phone' in user_data[message.chat.id] and 'service' not in user_data[message.chat.id])
def handle_service(message):
    chat_id = message.chat.id
    user_data[chat_id]['service'] = message.text.strip()

    submission = {
        "Имя": user_data[chat_id]['name'],
        "Телефон": user_data[chat_id]['phone'],
        "Описание": user_data[chat_id]['service'],
        "Дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        response = requests.post(SHEET_URL, json=submission)
        if response.status_code == 200:
            bot.send_message(chat_id, "✅ Заявка успешно отправлена! Мы скоро свяжемся.")
        else:
            bot.send_message(chat_id, f"⚠️ Ошибка при отправке: {response.status_code}")
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Произошла ошибка: {e}")

    # Очистка данных после отправки
    user_data.pop(chat_id, None)

# Запуск бота
bot.polling()
