import os
import replicate
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("8109093278:AAGD0KkdrnSsUiDP85_Nhho6OYibz3UkQLg")
REPLICATE_TOKEN = os.getenv("r8_DQwfkIKT5d22xGAch815HMpYhgJoqAN0n59QW")

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши описание, и я сгенерирую картинку 🎨")

# Обработка текста
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    try:
        output = replicate.run(
            "stability-ai/sdxl:latest",
            input={
                "prompt": prompt,
                "width": 768,
                "height": 768
            }
        )
        image_url = output[0]
        await update.message.reply_photo(photo=image_url)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Запуск приложения (без asyncio.run)
async def start_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    await app.initialize()
    await app.start()
    print("Бот запущен...")
    await app.updater.start_polling()
    await app.updater.idle()

# Хак для Render — запускаем внутри уже существующего event loop
import asyncio
asyncio.get_event_loop().create_task(start_bot())
