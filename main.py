import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import replicate

# Загружаем переменные из .env
load_dotenv()

# Получаем токены из окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Устанавливаем токен Replicate для API
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь команду /generate <запрос>, чтобы сгенерировать изображение.")

# Команда /generate <prompt>
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажи запрос. Пример: /generate cat in space")
        return

    prompt = " ".join(context.args)
    await update.message.reply_text("Генерирую изображение...")

    try:
        output = replicate.run(
            "stability-ai/stable-diffusion:db21e45e5b21fafd82c6c8aef6a5c7b016c31c758a534c80a3fec203d04e7c35",
            input={"prompt": prompt}
        )
        await update.message.reply_photo(photo=output[0])
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации: {e}")

# Основная функция запуска бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))

    print("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
