import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import replicate

# 🔐 ВСТАВЬ СЮДА СВОИ ТОКЕНЫ
BOT_TOKEN = "8109093278:AAGD0KkdrnSsUiDP85_Nhho6OYibz3UkQLg"
REPLICATE_API_TOKEN = "r8_EDwLsGh2o4jk0WyJfELNIxCXvLLeWnk01V45S"

# 🔐 Устанавливаем токен для replicate
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Логирование (по желанию)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Команда /generate
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши описание изображения после команды /generate")
        return

    prompt = " ".join(context.args)
    await update.message.reply_text("Генерирую изображение...")

    try:
        output = replicate.run(
            "stability-ai/stable-diffusion:db21e45b17e7e87d6cb5d2c7aa99cf0741dcce771b95c365d8502fcd203f6f78",
            input={"prompt": prompt}
        )
        await update.message.reply_text(output[0])
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации изображения: {e}")

# Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("generate", generate))
    app.run_polling()

if __name__ == "__main__":
    main()
