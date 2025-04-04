import os
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Получаем токены из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Устанавливаем API-ключ OpenAI
openai.api_key = OPENAI_API_KEY

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши описание, и я сгенерирую картинку 🎨")

# Генерация изображения
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        image_url = response.data[0].url
        await update.message.reply_photo(photo=image_url)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации: {e}")

# Запуск бота
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    application.run_polling()

if __name__ == "__main__":
    main()
