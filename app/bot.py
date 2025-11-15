import logging
import os
from dotenv import load_dotenv

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("API_URL")

NAME, PROFESSION, DESCRIPTION, PHOTO = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я бот для керування друзями.\n"
        "Команди:\n"
        "/list - список друзів\n"
        "/add - додати друга\n"
        "/friend <id> - деталі друга"
    )

async def list_friends(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        friends = response.json()
        if friends:
            text = ""
            for f in friends:
                text += f"{f['id']} - {f['name']} ({f['profession']})\n"
        else:
            text = "Список друзів порожній."
    except Exception as e:
        text = f"Помилка при отриманні друзів: {e}"
    await update.message.reply_text(text)

async def get_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Будь ласка, вкажіть ID друга.\nПриклад: /friend b984b170-f1b6-4878-a693-271ab1df50d2"
        )
        return

    friend_id = context.args[0]
    url = f"{API_URL}{friend_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        friend = response.json()

        text = (
            f"Ім'я: {friend['name']}\n"
            f"Професія: {friend['profession']}\n"
            f"Опис: {friend['profession_description'] or '—'}"
        )

        if friend.get('photo_url'):
            text += f"\nФото: {friend['photo_url']}"

        await update.message.reply_text(text)

    except Exception as e:
        await update.message.reply_text(
            f"Друг не знайдений або сталася помилка:\n{e}"
        )

async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введіть ім'я друга:")
    return NAME

async def add_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введіть ім'я друга:")
    return NAME

async def add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Введіть професію друга:")
    return PROFESSION

async def add_profession(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["profession"] = update.message.text
    await update.message.reply_text("Введіть опис професії (можна залишити порожнім):")
    return DESCRIPTION

async def add_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["profession_description"] = update.message.text
    await update.message.reply_text("Надішліть посилання на фото друга:")
    return PHOTO

async def add_friend_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("Будь ласка, надішліть фото саме як фото.")
        return PHOTO

    photo = update.message.photo[-1]
    file = await photo.get_file()

    file_path = f"Friend{update.message.from_user.id}.jpg"
    await file.download_to_drive(file_path)

    data = {
        "name": context.user_data["name"],
        "profession": context.user_data["profession"],
        "profession_description": context.user_data["profession_description"],
    }

    try:
        with open(file_path, "rb") as img:
            response = requests.post(
                API_URL,
                data=data,
                files={"photo_url": img},
            )
            response.raise_for_status()
            await update.message.reply_text("Друг успішно доданий і фото збережено!")

    except Exception as e:
        await update.message.reply_text(f"Помилка при додаванні друга: {e}")

    finally:
        import os
        if os.path.exists(file_path):
            os.remove(file_path)

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("add", add_friend)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_name)],
        PROFESSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_profession)],
        DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_description)],
        PHOTO: [MessageHandler(filters.PHOTO, add_friend_photo)],
    },
    fallbacks=[],
)



app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("list", list_friends))
app.add_handler(CommandHandler("friend", get_friend))
app.add_handler(conv_handler)

if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()