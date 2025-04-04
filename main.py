import os
import replicate
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Получаем токен из переменной окружения
REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not REPLICATE_TOKEN or not TELEGRAM_BOT_TOKEN:
    raise ValueError("Не заданы переменные окружения REPLICATE_API_TOKEN или TELEGRAM_BOT_TOKEN")

replicate_client = replicate.Client(api_token=REPLICATE_TOKEN)


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Напиши промпт после команды /generate")
        return

    try:
        await update.message.reply_text("Генерирую изображение...")

        output = replicate_client.run(
            "stability-ai/sdxl:latest",
            input={"prompt": prompt}
        )

        await update.message.reply_photo(photo=output[0])
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации изображения: {e}")


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("generate", generate))

    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
