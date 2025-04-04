import os
import replicate
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# API ключи
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

async def start(update: Update, context):
    await update.message.reply_text("Привет! Отправь описание изображения — и я его создам 🖼️")

async def generate_image(update: Update, context):
    prompt = update.message.text
    try:
        await update.message.reply_text("Генерирую... 🔄")

        output = replicate_client.run(
            "stability-ai/sdxl:latest",
            input={"prompt": prompt}
        )
        await update.message.reply_photo(photo=output[0])
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации: {e}")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except RuntimeError as e:
        if str(e).startswith("This event loop is already running"):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise
