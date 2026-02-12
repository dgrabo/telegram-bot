from dotenv import load_dotenv
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
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
    raise ValueError("BOT_TOKEN not loaded.")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Find restaurants", callback_data="find_restaurants")]]
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Option:", reply_markup=markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "find_restaurants":

        keyboard = [[KeyboardButton("Send Location", request_location=True)]]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await query.message.reply_text("Tekst", reply_markup=markup)

def main():
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()