import os
import openai
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Получаем ключи из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Устанавливаем API ключ OpenAI
openai.api_key = OPENAI_API_KEY

# /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Напиши описание, и я сгенерирую картинку 🎨")

# Генерация изображения
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

# Основной запуск
async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    await app.run_polling()

# Запуск с защитой от двойного event loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "already running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise
