import os
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Устанавливаем API-ключи через переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    await application.run_polling()

# Запуск бота с учетом особенностей Render
if __name__ == "__main__":
    import asyncio

    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
