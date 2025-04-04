import os
from dotenv import load_dotenv
import replicate
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем переменные из .env
load_dotenv()

# Получаем токены из .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_TOKEN = os.getenv("REPLICATE_TOKEN")

# Устанавливаем токен для Replicate
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши описание, и я сгенерирую картинку 🎨")

# Генерация изображения
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    try:
        output = replicate.run(
            "stability-ai/stable-diffusion:db21e45a03f5ec63dba47c3ef05c56d744e3c40c4110c8c720f3f52d4470a6f3",
            input={"prompt": prompt}
        )
        await update.message.reply_photo(photo=output[0])
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации: {e}")

# Основная функция
async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    await app.run_polling()

# Запуск
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
