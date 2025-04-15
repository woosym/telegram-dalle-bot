import os
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import openai

# Загружаем переменные окружения
load_dotenv()

# Получаем токены из .env файла
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Устанавливаем ключ API для OpenAI
openai.api_key = OPENAI_API_KEY

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Команда start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ИИ-бот 🤖. Напиши мне что-нибудь!")

# Обработчик сообщений от пользователей
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")

    try:
        # Отправляем запрос к OpenAI с использованием модели GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Используем GPT-4
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response['choices'][0]['message']['content']
        await update.message.reply_text(bot_reply)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text("Произошла ошибка при обращении к ИИ 😢")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Добавление обработчиков команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Бот запущен!")
    app.run_polling()
