import os
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Устанавливаем API-ключи через переменные окружения
TELEGRAM_TOKEN = os.getenv("8109093278:AAGD0KkdrnSsUiDP85_Nhho6OYibz3UkQLg")
OPENAI_API_KEY = os.getenv("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")

# Устанавливаем API-ключ OpenAI
openai.api_key = OPENAI_API_KEY

# Команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Напиши описание, и я сгенерирую картинку 🎨")

# Генерация изображения по сообщению
async def generate_image(update: Update, context):
    prompt = update.message.text
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        image_url = response['data'][0]['url']
        await update.message.reply_photo(photo=image_url)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации: {e}")

# Основная функция для запуска бота
async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    # Запуск бота
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
