from dotenv import load_dotenv
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters
)

load_dotenv()
token = os.getenv("BOT_TOKEN")
MENU, OPTION1, OPTION2 = range(3)

if not token:
    raise ValueError("BOT_TOKEN nije učitan.")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Pronađi resotrane", callback_data="find_restaurants")]]
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Opcija:", reply_markup=markup)

def main():
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()